# serise
# serise_id, title

# content
# content_id, serise_id

# view
# user_id, content_id, date, time

# 영상컨텐츠 사이트에서 시청데이터를 바탕으로 시리즈의 스코어 계산
# - 사용자가 시리즈의 컨텐츠를 얼마나 시청했는지 계산

from pyspark import SparkContext

sc = SparkContext()

serise_file_path = '/Users/kimminsu/dmf/spark/1.serise_data/serise.csv'
content_file_path = '/Users/kimminsu/dmf/spark/1.serise_data/content.csv'
view_file_path = '/Users/kimminsu/dmf/spark/1.serise_data/view.csv'

serise_rdd = sc.textFile(serise_file_path)
content_rdd = sc.textFile(content_file_path)
view_rdd = sc.textFile(view_file_path)

# serise_rdd.foreach(print)

serise = serise_rdd.map(lambda x: x.split(','))
content = content_rdd.map(lambda x: x.split(','))
view = view_rdd.map(lambda x: x.split(','))

# view.foreach(print)

# 1. 하나의 시리즈에 속한 컨텐츠 수
step1 = content.map(lambda x: (x[1], 1)) \
    .reduceByKey(lambda a, b: a+b)

# step1.foreach(print)

# 2. 재시청 카운트 x
step2 = view.map(lambda x: (x[1], x[0])).distinct()
# print(step2.count())
# step2.foreach(print)


# 3. content_id를 기준으로 join
# => (content_id, (user_id, serise_id))
# => step2(content_id, user_id) join content(content_id, serise_id)
step3 = step2.join(content)
# step3.foreach(print)

# 4. 유저당 시리즈 조회수 계산
step4 = step3.map(lambda x: (x[1], 1)) \
    .reduceByKey(lambda a, b: a+b)
# step4.foreach(print)

# 5. user_id 제거
step5 = step4.map(lambda x: (x[0][1], x[1]))
# step5.foreach(print)

# 6. step5의 결과와 step1의 결과를 join
step6 = step5.join(step1)
# step6.foreach(print)

# 7. 시리즈별 조회율 계산
step7 = step6.map(lambda x: (x[0], x[1][0]/x[1][1]))
# step7.foreach(print)

# 8. 점수화
# => serise_id, score
def get_score(row):
    serise_id = row[0]
    percentage = row[1]
    return serise_id, int(percentage * 100)

step8 = step7.map(get_score)
# step8.foreach(print)

# 9. 평균
step9 = step8.groupByKey().mapValues(lambda x: sum(x) / len(x))
# step9.foreach(print)

# 10. 시리즈와 join
step10 = step9.join(serise) \
    .map(lambda x: (x[1][1], x[1][0]))
# step10.foreach(print)

result = step10.collect()
result.sort(key=lambda x: x[1], reverse=True)

for r in result:
    print(r)