# -*- coding: utf-8 -*-
"""
@author: Duygu Bulut - b181210374
         & 
         Merve Bacak - b161210050
"""
#her sütun için gerekli bilgilerin tutulacağı listeler
all_events = [] 
all_times = []
all_from_nodes = []
all_to_nodes = []
all_pkt_type = []
all_pkt_size = []
all_flags = []
all_fids = []
all_src_addr = []
all_dest_addr = []
all_seq_nums =[]
all_pktid = []

'''tracefile'daki her bir sütunu elde etmek için dosyayı okurken
boşluklara gore parse edildi.'''
import codecs
with codecs.open("iz.tr", "r", "UTF8") as my_trace_file:
    my_trace_file=my_trace_file.readlines()
    
for line in my_trace_file:
    
    item = line.split(" ");
    #elde edilen sütun bilgileri oluşturulan listelere atıldı.
    all_events.append(item[0])
    all_times.append(item[1])
    all_from_nodes.append(item[2])  
    all_to_nodes.append(item[3]) 
    all_pkt_type.append(item[4]) 
    all_pkt_size.append(item[5]) 
    all_flags.append(item[6])  
    all_fids.append(item[7]) 
    all_src_addr.append(item[8])  
    all_dest_addr.append(item[9])  
    all_seq_nums.append(item[10])  
    all_pktid.append(item[11])  
   
'''dosya okunurken string olarak okunduğu için 
sayısal olan değerleri islem yapabilmek icin donusturmek gerekiyor.'''
all_times_f = [] # times float tipine donusecek

#zamanı floata cevirmek icin
for i in all_times:
    all_times_f.append(float(i))
       
#veriyi dataframe'e donusturmek icin pandas import edildi 
import pandas as pd

#elde edilen listeler dataframe'e atıldı
data = {'event': all_events,
        'times': all_times_f,
        'from_nodes' : all_from_nodes,
        'to_nodes' : all_to_nodes,
        'pkt_type' : all_pkt_type,
        'pkt_size' : all_pkt_size,
        'flags' : all_flags,
        'fids' : all_fids,
        'src_addr' : all_src_addr,
        'dest_addr' : all_dest_addr,
        'seq_nums' : all_seq_nums,
        'pkt_id' : all_pktid     
         }

#pdf hesaplamak icin gerekli fonksiyon yazildi
def calculate_pdf(send, received):    

    pdf = 0.0
    pdf = received / send
    return pdf

# DataFrame olusturuluyor
df = pd.DataFrame(data)
  
'''eventi r olan ve aynı islem zamanında gonderilmis olan veriyi
bir yerde toplamak ve packet delivery fraction hesaplamak icin while dongusunde
gerekli islemler yapildi, tum pdf degerleri hesaplandi'''
i=1
received_pkt = 0
total_times = 0.0 
pdf_list = [] #tum pdf degerlerini tutmak icin liste olusturuldu
times_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]    
temp_pdf = 0.0

while(i!= 20):  
    select_times =  df.loc[(df['event'] == 'r') & ((df['times']) >= i ) & ((df['times']) < i+1 )]
    select_received = (select_times.loc[(df['pkt_type'] == 'tcp')])
    #print(select_received)
    select_send = (select_times.loc[(df['pkt_type'] == 'ack')])
    #print(select_send)
    received_pkt = len(select_received.index)
    send_pkt = len(select_send.index)
    temp_pdf += calculate_pdf(send_pkt , received_pkt)
    #print(temp_pdf)
    pdf_list.append(temp_pdf)
    
    i = i+1

#print(pdf_list)  
# x ekseni zaman y ekseni packet delivery fraction olacak şekilde grafik çizdirildi    
import matplotlib.pyplot as plt
plt.plot(times_list, pdf_list)
plt.ylabel('packet delivery fraction')
plt.xlabel('times as seconds')
plt.title('Change of packet delivery fraction over time')
plt.show()
