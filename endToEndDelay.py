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

#delay hesaplamak icin gerekli fonksiyon yazildi
def calculate_delay(sendTimes, receivedTimes):    

    delay = 0.0
    delay = receivedTimes - sendTimes
    return delay

# DataFrame olusturuluyor
df = pd.DataFrame(data)
  
'''eventi r olan ve aynı islem zamanında gonderilmis olan veriyi
bir yerde toplamak ve delay hesaplamak icin while dongusunde
gerekli islemler yapildi, tum delay degerleri hesaplandi'''
i=1
received_pkt = 0
total_times = 0.0 
delay_list = [] #delay degerlerini tutmak icin liste olusturuldu
times_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]    
temp_delay = 0.0

while(i!= 20):
    select_times =  df.loc[(df['event'] == 'r') & ((df['times']) >= i ) & ((df['times']) < i+1 )]
    select_received = (select_times.loc[(df['pkt_type'] == 'tcp')])
    select_send = (select_times.loc[(df['pkt_type'] == 'ack')])
    times_received = select_received['times'].sum()
    times_send = select_send['times'].sum()
    #print(times_send)
    temp_delay = calculate_delay(times_send, times_received)
    #print(temp_delay)

    delay_list.append(temp_delay)   
    i = i+1
    
# x ekseni zaman y ekseni end to end delay olacak şekilde grafik çizdirildi
import matplotlib.pyplot as plt
plt.plot(times_list, delay_list)
plt.ylabel('delay as seconds')
plt.xlabel('times as seconds')
plt.title('Change of delay over time')
plt.show()

    



