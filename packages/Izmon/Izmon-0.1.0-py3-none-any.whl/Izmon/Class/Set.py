class Set:
    from .Basic.Common_Function import Common_Function as co_f
    from .Basic.Common_Variable import Common_Variable as co_v
    from .Save_Code.Encode import Encode as encode
    from .Save_Code.Decode import Decode as decode

    from .Basic.Settings import Settings as st

    def main(self):
        print("=" * self.st.SEPALATE_LEN)
        while True:
            action = self.co_f.typing("何をしますか？ 0:データコード名前変更 1:表示秒数変更 2:やめる", 1, 3)
            if action == 0:
                self.change_player_name()
            elif action == 1:
                self.change_show_length()
            else:
                break
            print("-" * self.st.SEPALATE_LEN)
        print("=" * self.st.SEPALATE_LEN)
        return

    def change_player_name(self):
        self.co_f.show("データコードに保存されているプレイヤー名を変更します。", 2) 
        code = self.co_f.typing("データコード", 0)
        data = self.decode(code, 1)
        code_new = self.encode(data)
        print("変更しました。")
        print("新しいコード：", code_new)
        return
    
    def change_show_length(self):
        length = self.co_f.typing("表示秒数を入力してください(最長10秒)", 1, 10)
        self.co_v.show_length = length
        print("設定しました。")
        return
