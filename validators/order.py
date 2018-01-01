from flask import request


class NewOrder(object):

    def validate(self):
        goods_list = request.form.getlist('goods[]')
        goods_quantity_list = request.form.getlist('goods_quantity[]')
        if len(goods_list) != len(goods_quantity_list):
            return False
        for index, goods in enumerate(goods_list):
            try:
                int(goods)
                int(goods_quantity_list[index])
            except (ValueError, IndexError):
                return False
        return True
