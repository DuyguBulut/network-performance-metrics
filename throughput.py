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
all_pkt_size_i = [] # size int tipine donusecek

#zamanı floata cevirmek icin
for i in all_times:
    all_times_f.append(float(i))
    
#packet size'i int'e cevirmek icin
for i in all_pkt_size:
    all_pkt_size_i.append(int(i))
    
#veriyi dataframe'e donusturmek icin pandas import edildi 
import pandas as pd

#elde edilen listeler dataframe'e atıldı
data = {'event': all_events,
        'times': all_times_f,
        'from_nodes' : all_from_nodes,
        'to_nodes' : all_to_nodes,
        'pkt_type' : all_pkt_type,
        'pkt_size' : all_pkt_size_i,
        'flags' : all_flags,
        'fids' : all_fids,
        'src_addr' : all_src_addr,
        'dest_addr' : all_dest_addr,
        'seq_nums' : all_seq_nums,
        'pkt_id' : all_pktid     
         }

#throughput hesaplamak icin gerekli fonksiyon yazildi
def calculate_throughput(total_bytes, total_times):    

    throughput = 0.0
    throughput = (total_bytes * 8) / (total_times * 1000)
    return throughput   

# DataFrame olusturuluyor
df = pd.DataFrame(data)
  
'''eventi r olan ve aynı islem zamanında gonderilmis olan veriyi
bir yerde toplamak ve throughput hesaplamak icin while dongusunde
gerekli islemler yapildi, tum throughput degerleri hesaplandi'''
i=1
temp_throughput = 0.0
total_times = 0.0 
total_size = 0
throughputs_list = [] #tum throughput degerlerini tutmak icin liste olusturuldu
times_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19] #saniyeler  

while(i!= 20):
    select_df =  df.loc[(df['event'] == 'r') & ((df['times']) >= i ) & ((df['times']) < i+1 )]
    total_times = select_df['times'].sum()
    total_size = select_df['pkt_size'].sum()
    #print("total time :" ,total_times)
    #print("total size: ", total_size)
    if(total_times !=0.0 and total_size != 0):
        #times_list.append(total_times)
        temp_throughput += calculate_throughput(total_size, total_times)
        throughputs_list.append(temp_throughput)
        total_times = 0.0 
        total_size = 0 
        #print("throughput: ",temp_throughput)
    i= i+1  

# x ekseni zaman y ekseni throughput olacak şekilde grafik çizdirildi
import matplotlib.pyplot as plt
plt.plot(times_list, throughputs_list)
plt.ylabel('throughputs as kbps')
plt.xlabel('times as seconds')
plt.title('Change of throughput over time')
plt.show()



