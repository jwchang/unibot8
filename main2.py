from typing import Set
from backend.core import run_llm2
from datetime import datetime

# 현재 시간을 가져옵니다
now = datetime.now()
print("현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S") )
prompt = '2023학년도 학사일정 알려줘'
generated_response = run_llm2( query=prompt )
print( generated_response['result'] )


# 현재 시간을 가져옵니다
now = datetime.now()
print("현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S") )
prompt = '졸업에 필요한 최소한의 학점에 대해 알려줘'
generated_response = run_llm2( query=prompt )
print( generated_response['result'] )


# 현재 시간을 가져옵니다
now = datetime.now()
print("현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S") )
prompt = '수강 신청은 어떻게 하나요'
generated_response = run_llm2( query=prompt )
print( generated_response['result'] )


# 현재 시간을 가져옵니다
now = datetime.now()
print("현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S") )
prompt = '신입생 장학제도에 대해 알려줘'
generated_response = run_llm2( query=prompt )
print( generated_response['result'] )

# 현재 시간을 가져옵니다
now = datetime.now()
print("현재 시간:", now.strftime("%Y-%m-%d %H:%M:%S") )

