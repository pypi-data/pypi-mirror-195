class End:
	from ..Basic.Common_Function import Common_Function as co_f
	from ..Basic.Settings import Settings as st
	
	def save(self): #データをセーブする
		from ..Save_Code import Encode
		while True:
			ty = self.co_f.typing("データをセーブしますか？ 1:する 0:しない", 1, 2)
			if ty == 1:
				code = Encode.encode()
				print("プレイヤー名と共に保管してください。")
				print("コード：", code)
				break
			else:
				break
		return