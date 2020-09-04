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

class ConvTas(nn.Module):
    def __init__(self, in_dim=1, enc_dim=512, window=32, shift=16, block_dim=128, block_kernel=3, hidden_dim=512, num_blocks=8, num_repeats=3, non_casual=8, casual=False):
        super(ConvTas, self).__init__()
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
        self.block_output = nn.Sequential(nn.PReLU(), nn.Conv1d(block_dim, enc_dim*1, kernel_size=1))
        self.mask_nl = nn.Sigmoid()
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
        norm1 = self.norm_1(conv1)
        conv2 = self.conv_2(norm1)
        
        output = conv2
        skip_connection = 0.
        for i in range(len(self.conv_blocks)):
            residual, skip = self.conv_blocks[i](output)
            output = output + residual
            skip_connection = skip_connection + skip

        output = self.block_output(skip_connection)
        masks = self.mask_nl(output).view(batch_size, 1, 512, -1)
        masked_output = conv1.unsqueeze(1)*masks

        output_speech = self.decoder_speech(masked_output[:,0,:,:])
        output_speech = output_speech[:,:,self.window-self.shift:-(rest+self.window-self.shift)].contiguous()
        output_speech = output_speech.view(batch_size, -1)

        return output_speech

def center_trim(tensor, reference):
    if hasattr(reference, "size"):
        reference = reference.size(-1)
    delta = tensor.size(-1) - reference
    if delta:
        tensor = tensor[..., delta // 2:-(delta - delta // 2)]
    return tensor

class UNet(nn.Module):
    def __init__(self, channels=64, kernel_size=8, stride=2, depth=5):
        super(UNet, self).__init__()
        self.encoder = nn.ModuleList()
        self.decoder = nn.ModuleList()
        in_channels = 1
        ch_scale = 2
        for indx in range(depth):
            e_block = nn.Sequential(
                nn.Conv1d(in_channels, channels, kernel_size=kernel_size, stride=stride),
                nn.ReLU(),
                nn.Conv1d(channels, ch_scale*channels, kernel_size=1, stride=1),
                nn.GLU(dim=1)
            )
            self.encoder.append(e_block)

            out_channels = in_channels if indx>0 else 1
            d_block = [nn.Conv1d(channels, ch_scale*channels, kernel_size=1, stride=1), nn.GLU(dim=1), nn.ConvTranspose1d(channels, out_channels, kernel_size=kernel_size, stride=stride)]
            if indx > 0:
                d_block += [nn.ReLU()]
            self.decoder.insert(0, nn.Sequential(*d_block))

            in_channels = channels
            channels = int(channels*ch_scale)
        
        channels = in_channels
        self.lstm = nn.LSTM(bidirectional=True, num_layers=2, hidden_size=channels, input_size=channels)
        self.linear = nn.Linear(2*channels, channels)
    def forward(self, x):
        x = x.unsqueeze(1)
        skip = []
        for e_block in self.encoder:
            x = e_block(x)
            skip.append(x)

        x = x.permute(2, 0, 1)
        x = self.lstm(x)[0]
        x = self.linear(x)
        x = x.permute(1, 2, 0)

        for d_block in self.decoder:
            s = center_trim(skip.pop(-1), x)
            x = x+s
            x = d_block(x)
        return x.view(x.size(0), 1, 1, x.size(-1))

if __name__ == "__main__":
    device = torch.device("cuda")
    inp = torch.randn(1, 1, 32000).to(device)
    model = UNet().to(device)