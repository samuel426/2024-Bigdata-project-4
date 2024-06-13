from  functions.function import gaussian, user_tomato_score, user_strawberry_score, find_tomato_near_row, find_strawberry_near_row
import os

#os.environ["SPARK_HOME"] = "/home/hadoop/spark"
#findspark.init()

#sc = pyspark.SparkContext(appName = "calc_score")
#sqlContext = SQLContext(sc)
#spark = SparkSession.builder.appName("untitled").getOrCreate()


class ReceiveData():
	def __init__(self, produce_info, input_dict):
		self.produce_type = produce_info
		self.produce_info = input_dict
		
	def get(self):
		if self.produce_type == 'tomato':
			score = user_tomato_score(
				self.produce_info['PFBS_NTRO_CBDX_CTRN'], 
				self.produce_info['EXTN_TPRT'], 
				self.produce_info['STRTN_WATER'], 
				self.produce_info['WATER_LACK_VL'], 
				self.produce_info['EXTN_ACCMLT_QOFLG'], 
				self.produce_info['NTSLT_SPL_PH_LVL'], 
				self.produce_info['NTSLT_SPL_ELCDT'], 
				self.produce_info['AVE_INNER_TPRT_1_2'], 
				self.produce_info['AVE_INNER_HMDT_1_2'])
			
			df_f = find_tomato_near_row(score)

		elif self.produce_type == 'strawberry':
			score = user_strawberry_score(
				self.produce_info['PFBS_NTRO_CBDX_CTRN'], 
				self.produce_info['EXTN_TPRT'], 
				self.produce_info['STRTN_WATER'], 
				self.produce_info['WATER_LACK_VL'], 
				self.produce_info['EXTN_ACCMLT_QOFLG'], 
				self.produce_info['AVE_INNER_TPRT_1_2'], 
				self.produce_info['AVE_INNER_HMDT_1_2'])
			
			df_f = find_strawberry_near_row(score)
			
		return df_f
