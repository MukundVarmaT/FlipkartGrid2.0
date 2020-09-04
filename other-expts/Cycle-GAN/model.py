import torch.nn as nn
import torch
import numpy as np
import torch.nn.functional as F

class up_2dsample(nn.Module):
    def __init__(self, upscale_factor=2):
        super(up_2dsample, self).__init__()
        self.scale_factor = upscale_factor
    def forward(self, inp):
        h = inp.shape[2]
        w = inp.shape[3]
        new_size = [h*self.scale_factor, w*self.scale_factor]
        return F.interpolate(inp, new_size)

class residuallayer(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(residuallayer, self).__init__()
        self.conv_layer = nn.Sequential(
                                        nn.Conv1d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        nn.InstanceNorm1d(num_features=out_channels, affine=True)
                                        )
        self.conv_layer_gate = nn.Sequential(
                                        nn.Conv1d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        nn.InstanceNorm1d(num_features=out_channels, affine=True)
                                        )
        self.conv_layer_output = nn.Sequential(
                                        nn.Conv1d(in_channels=out_channels, out_channels=in_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        nn.InstanceNorm1d(num_features=in_channels, affine=True)
                                        )
    def forward(self, inp):
        a = self.conv_layer(inp)
        b = self.conv_layer_gate(inp)
        c = a*torch.sigmoid(b)
        out = self.conv_layer_output(c)
        return inp + out

class downsample_generator(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(downsample_generator, self).__init__()
        self.conv_layer = nn.Sequential(
                                        nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        nn.InstanceNorm2d(num_features=out_channels, affine=True)
                                        )
        self.conv_layer_gate = nn.Sequential(
                                        nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        nn.InstanceNorm2d(num_features=out_channels, affine=True)
                                        )
    def forward(self, inp):
        a = self.conv_layer(inp)
        b = self.conv_layer_gate(inp)
        return a*torch.sigmoid(b)

class upsample_generator(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(upsample_generator, self).__init__()
        self.conv_layer = nn.Sequential(
                                        nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        up_2dsample(upscale_factor=2),
                                        nn.InstanceNorm2d(num_features=out_channels, affine=True)
                                        )
        self.conv_layer_gate = nn.Sequential(
                                        nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=stride, padding=padding),
                                        up_2dsample(upscale_factor=2),
                                        nn.InstanceNorm2d(num_features=out_channels, affine=True)
                                        )
    def forward(self, inp):
        a = self.conv_layer(inp)
        b = self.conv_layer_gate(inp)
        return a*torch.sigmoid(b)

class downsample_discriminator(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, stride, padding):
        super(downsample_discriminator, self).__init__()
        self.conv_layer = nn.Sequential(
                                    nn.Conv2d(in_channels=in_channels,out_channels=out_channels,kernel_size=kernel_size,stride=stride,padding=padding),
                                    nn.InstanceNorm2d(num_features=out_channels,affine=True)
                                    )
        self.conv_layer_gate = nn.Sequential(
                                        nn.Conv2d(in_channels=in_channels,out_channels=out_channels,kernel_size=kernel_size,stride=stride,padding=padding),
                                        nn.InstanceNorm2d(num_features=out_channels,affine=True)
                                        )
    def forward(self, inp):
        a = self.conv_layer(inp)
        b = self.conv_layer_gate(inp)
        return a*torch.sigmoid(b)

class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()

        self.conv_1 = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=[5,15], stride=1, padding=[2,7])
        self.conv_1_gate = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=[5,15], stride=1, padding=[2,7])

        self.downsample_1 = downsample_generator(in_channels=128, out_channels=256, kernel_size=5, stride=2, padding=2)
        self.downsample_2 = downsample_generator(in_channels=256, out_channels=512, kernel_size=5, stride=2, padding=2)

        self.conv_2 = nn.Conv1d(in_channels=3072, out_channels=512, kernel_size=1, stride=1)

        self.residuallayer_1 = residuallayer(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1)
        self.residuallayer_2 = residuallayer(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1)
        self.residuallayer_3 = residuallayer(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1)
        self.residuallayer_4 = residuallayer(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1)
        self.residuallayer_5 = residuallayer(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1)
        self.residuallayer_6 = residuallayer(in_channels=512, out_channels=1024, kernel_size=3, stride=1, padding=1)

        self.conv_3 = nn.Conv1d(in_channels=512, out_channels=3072, kernel_size=1, stride=1)

        self.upsample_1 = upsample_generator(in_channels=512, out_channels=512, kernel_size=5, stride=1, padding=2)
        self.upsample_2 = upsample_generator(in_channels=512, out_channels=512, kernel_size=5, stride=1, padding=2)

        self.conv_4 = nn.Conv2d(in_channels=512, out_channels=1, kernel_size=[5,15], stride=1, padding=[2,7])

    def forward(self, inp):
        
        inp = inp.unsqueeze(1)
        conv1 = self.conv_1(inp)*torch.sigmoid(self.conv_1_gate(inp))
        
        downsample1 = self.downsample_1(conv1)
        downsample2 = self.downsample_2(downsample1)

        downsample3 = downsample2.view([downsample2.shape[0], -1, downsample2.shape[3]])
        downsample3 = self.conv_2(downsample3)

        residual1 = self.residuallayer_1(downsample3)
        residual2 = self.residuallayer_2(residual1)
        residual3 = self.residuallayer_3(residual2)        
        residual4 = self.residuallayer_4(residual3)
        residual5 = self.residuallayer_5(residual4)
        residual6 = self.residuallayer_6(residual5)

        residual6 = self.conv_3(residual6)
        residual6 = residual6.view([downsample2.shape[0],downsample2.shape[1],downsample2.shape[2],downsample2.shape[3]])

        upsample1 = self.upsample_1(residual6)
        upsample2 = self.upsample_2(upsample1)

        output = self.conv_4(upsample2)
        output = output.view([output.shape[0],-1,output.shape[3]])
        return output

class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()

        self.conv_1 = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=[3,3], stride=[1,1])
        self.conv_1_gate = nn.Conv2d(in_channels=1, out_channels=128, kernel_size=[3,3], stride=[1,1])

        self.downsample_1 = downsample_discriminator(in_channels=128, out_channels=256, kernel_size=[3,3], stride=[2,2], padding=0)
        self.downsample_2 = downsample_discriminator(in_channels=256, out_channels=512, kernel_size=[3,3], stride=[2,2], padding=0)
        self.downsample_3 = downsample_discriminator(in_channels=512, out_channels=512, kernel_size=[3,3], stride=[2,2], padding=0)
        self.downsample_4 = downsample_discriminator(in_channels=512, out_channels=512, kernel_size=[1,5], stride=[1,1], padding=[0,2])
        
        self.output_layer = nn.Conv2d(in_channels=512, out_channels=1, kernel_size=[1,3], stride=[1,1], padding=[0,1])
    
    def forward(self, inp):

        inp = inp.unsqueeze(1)
        pad_input = nn.ZeroPad2d((1, 1, 1, 1))
        layer1 = self.conv_1(pad_input(inp)) * torch.sigmoid(self.conv_1_gate(pad_input(inp)))

        pad_input = nn.ZeroPad2d((1, 0, 1, 0))
        downsample1 = self.downsample_1(pad_input(layer1))
        pad_input = nn.ZeroPad2d((1, 0, 1, 0))
        downsample2 = self.downsample_2(pad_input(downsample1))
        pad_input = nn.ZeroPad2d((1, 0, 1, 0))
        downsample3 = self.downsample_3(pad_input(downsample2))
        downsample4 = self.downsample_4(downsample3)

        output = self.output_layer(downsample4)

        output = output.contiguous().permute(0, 2, 3, 1).contiguous()
        output = torch.sigmoid(output)
        return output

if __name__ == '__main__':
    device = torch.device("cuda")
    np.random.seed(0)
    input = np.random.randn(15, 24, 128)
    input = torch.from_numpy(input).float().to(device)
    generator = Generator().to(device)
    output = generator(input)
    print("Output shape Generator", output.shape)
    
    discriminator = Discriminator().to(device)
    output = discriminator(output)
    print("Output shape Discriminator", output.shape)