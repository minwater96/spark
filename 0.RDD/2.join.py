from pyspark import SparkContext

sc = SparkContext()

user_file_path = 'file:///Users/kimminsu/dmf/spark/0.RDD/user.csv'
post_file_path = 'file:///Users/kimminsu/dmf/spark/0.RDD/post.txt'

lines_user = sc.textFile(user_file_path)
lines_post = sc.textFile(post_file_path)

parsed_user_rdd = lines_user.map(lambda line: line.split(','))
parsed_post_rdd = lines_post.map(lambda line: line.split('\t'))

# parsed_post_rdd.foreach(print)

# (user_id, user)
user_tuple = parsed_user_rdd.map(lambda user: (user[0], user))
# user_tuple.foreach(print)

# (user_id, post)
post_tuple = parsed_post_rdd.map(lambda post: (post[2], post))

joined_rdd = user_tuple.join(post_tuple)
# joined_rdd.foreach(print)


# email .com으로 끝나는 사용자가 작성한 post만 필터링
def filter_com(line):
    email = line[1][0][3]
    return email.endswith('.com')

filtered_rdd = joined_rdd.filter(filter_com) \
    .map(lambda line: (line[0], line[1][1][0]) )
filtered_rdd.foreach(print)


