#import libraries
import torch
import torch.nn as nn
import torch.nn.functional as F


class DownSamplingLayer(nn.Module):
    def __init__(self, channel_in, channel_out, dilation=1, kernel_size=15, stride=1, padding=7):
        super(DownSamplingLayer, self).__init__()

        self.down_sampling_block = nn.Sequential(
            nn.Conv1d(channel_in, channel_out, kernel_size=kernel_size, stride=stride, padding=padding, dilation=dilation),
            nn.BatchNorm1d(channel_out),
            nn.LeakyReLU(negative_slope=0.1)
        )

    def forward(self, x):
        return self.down_sampling_block(x)

class UpSamplingLayer(nn.Module):
    def __init__(self, channel_in, channel_out, kernel_size=5, stride=1, padding=2):
        super(UpSamplingLayer, self).__init__()

        self.up_sampling_block = nn.Sequential(
            nn.Conv1d(channel_in, channel_out, kernel_size=kernel_size, stride=stride, padding=padding),
            nn.BatchNorm1d(channel_out),
            nn.LeakyReLU(negative_slope=0.1, inplace=True),
        )

    def forward(self, x):
        return self.up_sampling_block(x)

class Model(nn.Module):
    def __init__(self, n_layers=12, channels_interval=24):
        super(Model, self).__init__()

        self.n_layers = n_layers
        self.channels_interval = channels_interval

        encoder_in_channels_list = [1] + [i * self.channels_interval for i in range(1, self.n_layers)]
        encoder_out_channels_list = [i * self.channels_interval for i in range(1, self.n_layers + 1)]

        #print(encoder_in_channels_list)
        #print(encoder_out_channels_list)

        #initialize encoder
        self.encoder = nn.ModuleList()
        for i in range(self.n_layers):
            self.encoder.append(DownSamplingLayer(channel_in=encoder_in_channels_list[i], channel_out=encoder_out_channels_list[i]))

        #initialize bottle_neck layer
        self.bottle_neck = nn.Sequential(
            nn.Conv1d(self.n_layers * self.channels_interval, self.n_layers * self.channels_interval, 15, stride=1, padding=7),
            nn.BatchNorm1d(self.n_layers * self.channels_interval),
            nn.LeakyReLU(negative_slope=0.1, inplace=True)
        )

        decoder_in_channels_list = [(2 * i + 1) * self.channels_interval for i in range(1, self.n_layers)] + [2 * self.n_layers * self.channels_interval]
        decoder_in_channels_list = decoder_in_channels_list[::-1]
        decoder_out_channels_list = encoder_out_channels_list[::-1]

        #print(decoder_in_channels_list)
        #print(decoder_out_channels_list)

        #initialize decoder
        self.decoder = nn.ModuleList()
        for i in range(self.n_layers):
            self.decoder.append(UpSamplingLayer(channel_in=decoder_in_channels_list[i], channel_out=decoder_out_channels_list[i]))

        #initialize final output layer
        self.out = nn.Sequential(
            nn.Conv1d(1 + self.channels_interval, 1, kernel_size=1, stride=1),
            nn.Tanh()
        )

    def forward(self, input):
        tmp = []
        out = input

        # Up Sampling
        for i in range(self.n_layers):
            out = self.encoder[i](out)
            #print("Encoder Shape : " , o.shape)
            tmp.append(out)
            # [batch_size, T // 2, channels]
            out = out[:, :, ::2]
            #print("Encoder Reshape Shape : " , o.shape)

        out = self.bottle_neck(out)    # Bottle_Neck

        # Down Sampling
        for i in range(self.n_layers):
            
            out = F.interpolate(out, scale_factor=2, mode="linear", align_corners=True)   # [batch_size, T * 2, channels]

            out = torch.cat([out, tmp[self.n_layers - i - 1]], dim=1)  # Skip Connection
            
            out = self.decoder[i](out)  #Decoder

        out = torch.cat([out, input], dim=1)
        out = self.out(out)

        return out

'''
model = Model()
inp = torch.rand((17,1,16384))
output = model(inp)
print("Output Shape : " , output.shape)
'''