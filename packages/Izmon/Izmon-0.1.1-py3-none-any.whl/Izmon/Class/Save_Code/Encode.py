class Encode:
	def encode(data : str = ""):
		from ..Basic.Settings import Settings as st
		from ..Basic.Common_Variable import Common_Variable as co_v
		import hashlib
		if data == "":
			for i in range(100):
				if i >= st.IZ_NUM:
					data += "0"
				else:
					data += str(co_v.fellows[i])
		data_10 = str(int(data, 2))
		player_hash = str(int(hashlib.sha256(co_v.player_name.encode("utf-8")).hexdigest(), 16))
		data_hash_add = data_10 + player_hash[:20]
		check_digit = int(data_hash_add) % int(player_hash[21])
		data_check_add = int(data_hash_add + str(check_digit))
		code_16 = format(data_check_add, "0x")
		return code_16