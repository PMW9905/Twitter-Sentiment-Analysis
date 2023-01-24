import findspark
findspark.init()

import json

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

from textblob import TextBlob

#from elasticsearch import Elasticsearch

def getPolarity(text):
    sntmnt = TextBlob(text).sentiment.polarity
    if sntmnt > 0.1:
        sntmnt = 1
    elif sntmnt < -.1:
        sntmnt = -1
    else:
        sntmnt = 0
    return (text, sntmnt)


if __name__=="__main__":
    #setting up pyspark
    conf = SparkConf().setMaster("local").setAppName("My App")
    sc = SparkContext(conf = conf)
    ssc = StreamingContext(sc,15)

    #setting up elastisearch
    # es = Elasticsearch(hosts=["https://localhost:9200"])
    # es_conf = { "es.resource" : "tsd/mem","es.input.json" : "true"}

    #creating consumer
    message=KafkaUtils.createDirectStream(ssc,topics=['tweets'],kafkaParams={"metadata.broker.list":"localhost:9092"})

    analysed_words = message.map(lambda x: getPolarity(x[1]))
    analysed_words.pprint()
    # format_to_dict = analysed_words.map(lambda x: {"text": x[0], "pol": x[1]})
    # formatted_data = format_to_dict.map(lambda x: (None,x))
    # formatted_data.foreachRDD(lambda line: line.saveAsNewAPIHadoopFile(
    #     path="-", 
    #     outputFormatClass="org.elasticsearch.hadoop.mr.EsOutputFormat",
    #     keyClass="org.apache.hadoop.io.NullWritable",
    #     valueClass="org.elasticsearch.hadoop.mr.LinkedMapWritable",
    #     conf=es_conf
    # ))

    ssc.start()
    ssc.awaitTermination()