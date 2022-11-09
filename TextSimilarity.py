import sys
import re
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from konlpy.tag import Okt
from gensim.models import doc2vec
from gensim.models.doc2vec import TaggedDocument
from tqdm import tqdm

#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("TextSimilarity.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_result)
        self.text = str()
        self.tabWidget.setCurrentIndex(0)
        table = self.tableWidget
        table.setColumnWidth(0, 300)
        table.setColumnWidth(1, 300)
        table.setColumnWidth(2, 80)

    def get_Doc2Vec(self):
        tagger = Okt()
        df = pd.read_excel("./context.xlsx", engine="openpyxl", header=0)
        tagged_corpus_list=[]
        for index, row in tqdm(df.iterrows(), total=len(df)):
            text = row.iloc[1]
            tag = row.iloc[0]
            tagged_corpus_list.append(TaggedDocument(tags=[tag], words=tagger.morphs(text)))
        
        model = doc2vec.Doc2Vec(vector_size=360, alpha=0.025, min_alpha=0.025, workers=8, window=8)
        model.build_vocab(tagged_corpus_list)
        model.train(corpus_iterable=tagged_corpus_list, total_examples=model.corpus_count, epochs=50)
        model.save('./coverLetter.doc2vec')
        return df, model
    
    def check_Doc2Vec(self, len_df):
        df, model = self.get_Doc2Vec()
        range_df = len(df.loc[df['docNo'] == len_df])
        self.tableWidget.setRowCount(range_df)
        count = 0
        for i in range(len(df)):
            if df.iloc[i, 2] == len_df:
                self.tableWidget.setItem(count, 0, QTableWidgetItem(df.iloc[i, 1]))
                similar_doc = model.dv.most_similar(i)
                similar_idx = similar_doc[0][0]
                similar_rate = similar_doc[0][1]
                if similar_rate >= 0.7:
                    self.tableWidget.setItem(count, 1, QTableWidgetItem(df.iloc[similar_idx, 1]))
                    self.tableWidget.setItem(count, 2, QTableWidgetItem(str(round(similar_rate * 100, 2))))
                count += 1

    def print_result(self):
        self.text = re.sub(r"[^가-힣A-Za-z0-9\. ]", "", self.text)
        df = pd.read_excel("./df_sample07.xlsx", engine="openpyxl", header=0, index_col=0)
        len_df = len(df)
        school_code = 0
        if 6 <= self.comboBox.currentIndex() < 20:
            school_code = 1
        elif 20 <= self.comboBox.currentIndex() < 24:
            school_code = 2
        elif 24 <= self.comboBox.currentIndex() < 28:
            school_code = 3
        new_data = {
            '내용': self.plainTextEdit.toPlainText(),
            '학교': self.comboBox.currentText(),
            'school_code' : school_code,
            '전공' : self.comboBox_2.currentText(),
            'major_code' : self.comboBox_2.currentIndex(),
            '진로' : self.comboBox_3.currentText(),
            'career_code' : self.comboBox_3.currentIndex(),
            '인성' : self.comboBox_4.currentText(),
            'personal_code' : self.comboBox_4.currentIndex()
        }
        df_2 = pd.DataFrame(data=new_data, index=[len(df)])
        df = pd.concat([df, df_2])
        df.to_excel("./df_sample07.xlsx")
        content = df['내용']
        context = pd.DataFrame()
        for i in range(len(content)):
            text = content[i]
            text.lower()
            texts = text.split(". ")
            for text in texts:
                if len(text) <= 5:
                    continue
                text = re.sub(r"[^가-힣a-zA-Z0-9 ]", "", text)
                temp_df = pd.DataFrame({0:[text], 1:[i]})
                context = pd.concat([context, temp_df], ignore_index = True)
        context.columns = ['text', 'docNo']
        context.to_excel("context.xlsx")
        self.check_Doc2Vec(len_df)
        self.tabWidget.setCurrentIndex(1)

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()