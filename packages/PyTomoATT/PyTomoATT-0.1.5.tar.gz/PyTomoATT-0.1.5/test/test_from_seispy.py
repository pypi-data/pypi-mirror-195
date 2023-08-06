from pytomoatt.src_rec import SrcRec


def sub_case01(path):
    # Download test data from https://osf.io/xghrk/download
    sr = SrcRec.from_seispy(path)
    sr.write('src_rec_seispy')


if __name__ == '__main__':
    path = '/Users/xumijian/Codes/seispy-example/ex-ccp/RFresult'
    sub_case01(path)