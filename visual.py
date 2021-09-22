import os
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.pyplot import MultipleLocator
from csv_parser import Parse_txt


class Visualize(object):
    
    def __init__(self):
        print('abcd')
        self.iostat_list = [x for x in os.listdir() if x.endswith('csv')]
        li_io = []
        for io_file in self.iostat_list:
            li_io.append(pd.read_csv(io_file))

        self.df = pd.concat(li_io)
        self.device_name = self.df.columns[0]
        self.original_sd = self.df[self.device_name].unique()
        
        self.columns = self.df.columns
        if 'w_await' in self.columns:
            self.list_to_analise = ['r/s', 'w/s', 'rMB/s', 'wMB/s', 'r_await', 'w_await', 'svctm']
            self.list_all_analise = ['r/s', 'w/s', 'rMB/s', 'wMB/s', 'r_await', 'w_await', 'svctm', 'rrqm/s', 'wrqm/s',
                                'avgre-sz']
        else:
            self.list_to_analise = ['r/s', 'w/s', 'rMB/s', 'wMB/s', 'await', 'svctm']
            self.list_all_analise = ['r/s', 'w/s', 'rMB/s', 'wMB/s', 'await', 'svctm', 'rrqm/s', 'wrqm/s',
                                'avgre-sz']
        
    def interact(self):
        while 1:
            disks = input("请输入要分析的逻辑盘符，用逗号隔开，开头和结尾不需要用逗号\n分析所有盘符直接输入1后回车。")
            if disks == 1:
                disks = self.original_sd
                break
            else:
                disks = disks.split(',')
                print("确认您需要分析的盘符为{}\n确认输入y，重写输入n。".format(disks))
                answer = input("请输入y或者n后回车。")

                confirmed_sd = [i for i in disks if i in self.original_sd]  # 校验盘符

                if answer == 'y' and len(confirmed_sd) == len(disks):
                    break
                else:
                    print('检查盘符输入是否有错误')
                    continue

        while 1:
            print("可分析的iostat指标为{}".format(self.columns))
            print("默认分析指标为'r/s', 'w/s', 'rMB/s', 'wMB/s', 'await', 'svctm'")

            zhibiao = input('请再次手动输入您要多分析的指标后回车，如只分析默认指标，请直接回车。')
            zhibiao = zhibiao.split(',')
            answer = input("您需要分析的指标为{}？\n确认请输入y后回车，重写请输入n后回车".format(str(zhibiao)))
            x_len = input("请输入导出图片的X轴坐标间隔单位，请输入整数后回车，无需添加标点和空格，\n本参数输入多少可参考压测模型的runtime。")

            confirmed_zhibiao = [i for i in zhibiao if i in self.list_all_analise]
            if answer == 'y' and len(confirmed_zhibiao) == len(zhibiao):
                self.list_to_analise.extend(zhibiao)
                break

            else:
                print('检查指标是否写对了。')
                continue

        print("开始分析，针对{}盘符，进行{}指标的分析绘图。".format(str(disks), str(self.list_to_analise)))
        return disks, x_len
    
    def draw(self, *args):
        sd_group = self.df.groupby(self.device_name)
        df_list = []

        """for i in sd_group， i[1] 是可分析的数据
            跟用户交互时，用户直接回车会形成空串，因此下面会用到.remove
            盘符List长度 == 画图时候的长
            分析字段的List长度  == 画图时候的宽
            count2 = 画图时候的子图数量
            tie = 画图标题
        """

        for i in sd_group:
            df1 = i[1]
            df_list.append(df1)

        try:
            self.list_to_analise.remove('')
        except Exception as e:
            print('e')
            pass

        list_target = args[0][0]
        length_target = len(list_target)
        length_zhibiao = len(self.list_to_analise)
        # row_number = length_zhibiao * length_target // 5 + 1
        count2 = 0

        fig2 = plt.figure(figsize=(4 * length_zhibiao, 4 * length_target))

        for data in df_list:
            data = data.reset_index()
            df_title = data.iloc[1:2, :]

            tie = df_title[self.device_name].values[0]

            if tie in list_target:

                for name in self.list_to_analise:
                    count2 += 1
                    ax2 = fig2.add_subplot(length_target, length_zhibiao, count2)
                    plt.title("{}{}".format(tie, name))
                    x_major_locator = MultipleLocator(int(args[0][1]))
                    ax = plt.gca()
                    ax.xais.set_major_locator(x_major_locator)
                    plt.plot(data.index, data[name], label=tie)
                    plt.xticks(rotation=270)
                    plt.legend()

            pass
        plt.savefig('./iostat.png')

        print('正在绘图')
        return df_list

    def clean_up(self, df_list):
        # 绘图后的整理,超过100W行的数据会按照盘符来分sheet呈现

        if len(self.df) > 1000000:
            writer = pd.ExcelWriter('./iostat测试数据.xlxs')
            self.df.to_excel(writer, sheet_name='数据', index=False)

            sheet = writer.book.add_worksheet('图片')
            sheet.insert_image('A1', 'iostat.png')
            writer.save()

        for waste in self.iostat_list:
            os.remove(waste)

        else:

            writer = pd.ExcelWriter('./iostat测试数据.xlxs')
            for data in df_list:
                data = data.reset_index()
                df_title = data.iloc[1:2, :]
                tie = df_title[self.device_name].values[0]

                data.to_excel(writer, sheet_name=tie, index=False)
                sheet = writer.book.add_worksheet('图片')
                sheet.insert_image('A1', 'iostat.png')
                writer.save()

            for waste in self.iostat_list:
                os.remove(waste)

        return None


if __name__ == '__main__':
    current_path = os.getcwd()
    parse = Parse_txt(current_path)
    files = parse.get_path()
    parse.to_csv(files)

    a = Visualize()
    while 1:
        b = a.interact()
        c = a.draw(b)
        a.clean_up(c)

        os.remove('iostat.png')
        again = input('重新分析一次？y/n')
        if again == 'y':
            continue
        break



