
def get_symbol(index):
    return "/html/body/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[3]/tbody/tr[{index}]/td[4]/b/a".format(index=index)

def get_change(index):
    return "/html/body/table[1]/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[3]/tbody/tr[{index}]/td[6]/b/span/font".format(index=index)
