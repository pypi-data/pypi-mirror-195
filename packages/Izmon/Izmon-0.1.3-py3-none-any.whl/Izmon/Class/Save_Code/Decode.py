class Decode:
	def decode(code : str, typ : int):
		import hashlib
		from ..Basic.Common_Variable import Common_Variable as co_v
		from ..Basic.Settings import Settings as st
		
		player_hash = str(int(hashlib.sha256(co_v.player_name.encode("utf-8")).hexdigest(), 16))
		code_10 = str(int(code, 16))
		if int(str(code_10)[:-1]) % int(player_hash[21]) != int(str(code_10)[-1]):
			return 0
		code_10_str = str(code_10)
		if code_10_str[-21:-1] != player_hash[:20]:
			return 0
		data = format(int(code_10_str[:-21]), str(st.IZ_NUM) + 'b')
		if typ == 0:
			for i in range(100):
				if i >= st.IZ_NUM:
					continue
				else:
					co_v.fellows[i] = int(data[i])
			return 1
		else:
			return data