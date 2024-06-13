

class ReceiveData():
    def __init__(self, produce_info, input_dict):
        self.produce_info = produce_info
        self.number = input_dict

    def sendQueryToHDFS(self):
        '''
        사용자가 입력한 input을 바탕으로 query를 spark? HDFS?에 날림
        결과는 데이터 분석이 완료된 결과 파일을 받아오면 되지 않을까
        '''
        #f_path = '규칙에따라만들어진결과파일'
        f_path = 'strawberry_avg.csv'
        return f_path