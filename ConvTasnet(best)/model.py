import torch
import torch.nn as nn
import numpy as np

class ChannelWiseLayerNorm(nn.Module):
    def __init__(self, dim, eps=1e-8):
        super(ChannelWiseLayerNorm, self).__init__()
        self.gain = nn.Parameter(torch.ones(1, dim, 1))
        self.bias = nn.Parameter(torch.zeros(1, dim, 1))
        self.eps = eps

    def forward(self, x):
        batch_size = x.size(0)
        channel = x.size(1)
        time_step = x.size(2)
        step_sum = x.sum(1)  # B, T
        step_pow_sum = x.pow(2).sum(1)  # B, T
        cum_sum = torch.cumsum(step_sum, dim=1)  # B, T
        cum_pow_sum = torch.cumsum(step_pow_sum, dim=1)  # B, T
        entry_cnt = np.arange(channel, channel*(time_step+1), channel)
        entry_cnt = torch.tensor(entry_cnt,dtype=torch.float,device=x.device).type(x.type())
        entry_cnt = entry_cnt.view(1, -1).expand_as(cum_sum)
        cum_mean = cum_sum / entry_cnt  # B, T
        cum_var = (cum_pow_sum - 2*cum_mean*cum_sum) / entry_cnt + cum_mean.pow(2)  # B, T
        cum_std = (cum_var + self.eps).sqrt()  # B, T
        cum_mean = cum_mean.unsqueeze(1)
        cum_std = cum_std.unsqueeze(1)
        x = (x - cum_mean.expand_as(x)) / cum_std.expand_as(x)
        return x * self.gain.expand_as(x).type(x.type()) + self.bias.expand_as(x).type(x.type())

class ConvBlock(nn.Module):
    def __init__(self, in_dim, hidden_dim, kernel_size, padding, dilation, casual=False):
        super(ConvBlock, self).__init__()
        self.conv_1 = nn.Conv1d(in_dim, hidden_dim, kernel_size=1)
        self.casual = casual
        if casual:
            self.padding = (kernel_size-1)*dilation
        else:
            self.padding = padding
        self.conv_2 = nn.Conv1d(hidden_dim, hidden_dim, kernel_size, dilation=dilation, groups=hidden_dim, padding=self.padding)
        self.conv_3 = nn.Conv1d(hidden_dim, in_dim, kernel_size=1)
        self.activ_1 = nn.PReLU()
        self.activ_2 = nn.PReLU()
        self.norm_1 = ChannelWiseLayerNorm(hidden_dim, eps=1e-08)
        self.norm_2 = ChannelWiseLayerNorm(hidden_dim, eps=1e-08)
        self.conv_4 = nn.Conv1d(hidden_dim, in_dim, kernel_size=1)
        
    def forward(self, x):
        conv1 = self.conv_1(x)
        activ1 = self.activ_1(conv1)
        norm1 = self.norm_1(activ1)
        if self.casual:
            conv2 = self.conv_2(norm1)[:,:,:-self.padding]
        else:
            conv2 = self.conv_2(norm1)
        activ2 = self.activ_2(conv2)
        norm2 = self.norm_2(activ2)

        residual = self.conv_3(norm2)
        skip = self.conv_4(norm2)
        return residual, skip

class Model(nn.Module):
    def __init__(self, delay_frame = 31, in_dim=1, enc_dim=512, window=32, shift=16, block_dim=128, block_kernel=3, hidden_dim=512, num_blocks=8, num_repeats=3, non_casual=5, casual=True):
        super(Model, self).__init__()
        self.delay_frame = delay_frame
        self.window = window
        self.shift = shift
        self.enc_dim = enc_dim
        self.conv_1 = nn.Conv1d(in_dim, enc_dim, kernel_size=window, bias=False, stride=shift)
        if casual:
            self.norm_1 = ChannelWiseLayerNorm(enc_dim, eps=1e-8)
        else:
            self.norm_1 = nn.GroupNorm(1, enc_dim, eps=1e-8)
        self.conv_2 = nn.Conv1d(enc_dim, block_dim, kernel_size=1)

        self.conv_blocks = nn.ModuleList()
        count = 0
        for i in range(num_repeats):
            for j in range(num_blocks):
                if count<non_casual:
                    self.conv_blocks.append(ConvBlock(block_dim, hidden_dim, kernel_size=block_kernel, padding=2**j, dilation=2**j))
                else:
                    self.conv_blocks.append(ConvBlock(block_dim, hidden_dim, kernel_size=block_kernel, padding=2**j, dilation=2**j, casual=True))
                count+=1
        self.block_output = nn.Sequential(nn.PReLU(), nn.Conv1d(block_dim, enc_dim*2, kernel_size=1))
        self.mask_nl = nn.Sigmoid()
        self.decoder_noise = nn.ConvTranspose1d(enc_dim, 1, kernel_size=window, bias=False, stride=shift)
        self.decoder_speech = nn.ConvTranspose1d(enc_dim, 1, kernel_size=window, bias=False, stride=shift)

    def forward(self, x):
        x = x.unsqueeze(1)
        batch_size, length = x.size(0), x.size(2)
        rest = self.shift - (length - self.window)%self.shift
        if rest > 0:
            pad = torch.tensor(np.zeros((batch_size, 1, rest)), dtype=torch.float, device=x.device)
            x = torch.cat([x, pad], 2)
        pad_aux = torch.tensor(np.zeros((batch_size,1,self.window-self.shift)),dtype=torch.float,device=x.device).type(x.type())
        x = torch.cat([pad_aux, x, pad_aux], 2)
        conv1 = self.conv_1(x)
        pad = torch.tensor(np.zeros([batch_size,self.enc_dim,self.delay_frame]),dtype=torch.float,device=x.device).type(x.type())
        conv1 = torch.cat([pad, conv1, pad], 2)
        norm1 = self.norm_1(conv1)
        conv2 = self.conv_2(norm1)
        
        output = conv2
        skip_connection = 0.
        for i in range(len(self.conv_blocks)):
            residual, skip = self.conv_blocks[i](output)
            output = output + residual
            skip_connection = skip_connection + skip

        output = self.block_output(skip_connection)
        masks = self.mask_nl(output).view(batch_size, 2, 512, -1)
        masked_output = conv1.unsqueeze(1)*masks

        if self.delay_frame:
            masked_output = masked_output[:,:,:,self.delay_frame:-self.delay_frame]

        output_speech = self.decoder_speech(masked_output[:,0,:,:])
        output_speech = output_speech[:,:,self.window-self.shift:-(rest+self.window-self.shift)].contiguous()
        output_speech = output_speech.view(batch_size, -1)

        output_noise = self.decoder_noise(masked_output[:,1,:,:])
        output_noise = output_noise[:,:,self.window-self.shift:-(rest+self.window-self.shift)].contiguous()
        output_noise = output_noise.view(batch_size, -1)

        return [output_speech, output_noise]

if __name__ == "__main__":
    device = torch.device("cuda")
    inp = torch.randn(1, 32000).to(device)
    model = Model().to(device)
    out = model(inp)
    print("output shape is {}".format([o.shape for o in out]))