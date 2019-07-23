import torch

class CNN1d(torch.nn.Module):
    def __init__(self,input_size,conv_seq_len,hidden_size,conv_kernel,pool_kernel ,padding=[0,0],
                 stride=1,dilation=1, dropout=0.0,output_size=1):
        super(CNN1d, self).__init__()

        self.num_layers=len(hidden_size)
        self.conv1=torch.nn.utils.weight_norm(
            torch.nn.Conv1d(input_size,hidden_size[0],conv_kernel[0],stride=1,padding=padding[0],dilation=dilation[0]))
        self.relu1=torch.nn.ReLU()
        self.pool1=torch.nn.MaxPool1d(pool_kernel[0],pool_kernel[0],padding[0],dilation=1)
        if self.num_layers > 1:
            self.drop1=torch.nn.Dropout(dropout)
            self.conv2=torch.nn.utils.weight_norm(
                torch.nn.Conv1d(hidden_size[0],hidden_size[1],conv_kernel[1],stride=1,padding=padding[0],dilation=dilation[1]))
            self.relu2=torch.nn.ReLU()
            self.pool2=torch.nn.MaxPool1d(pool_kernel[1],pool_kernel[1],padding[1],dilation=1)

        self.drop2=torch.nn.Dropout(dropout)
        self.linear1=torch.nn.Linear(conv_seq_len,output_size)
        """self.relu2=torch.nn.ReLU()
        self.drop3=torch.nn.Dropout(dropout)
        self.linear2=torch.nn.Linear(10,output_size)    """
        self.sigmoid=torch.nn.Sigmoid()
    def forward(self,subject):
        c1=self.conv1(subject)
        r1=self.relu1(c1)
        p1=self.pool1(r1)

        if self.num_layers > 1:
            drop1=self.drop1(p1)
            c2=self.conv2(drop1)
            r2=self.relu2(c2)
            p2=self.pool2(r2)
            #flatten
            flat=p2.view(p2.size(0), -1)
        else:
            flat=p1.view(p1.size(0), -1)
        drop2=self.drop2(flat)
        l1=self.linear1(drop2)

        """r2=self.relu2(l1)
        drop3=self.drop3(r2)
        l2=self.linear2(drop3)"""
        #l3=self.linear3(drop2)
        return self.sigmoid(l1)
