from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)
# openai.api_key = ''
url = 'https://www.youtube.com/watch?v=UCGaKvZpJYc'
print(url)

video_id = url.replace('https://www.youtube.com/watch?v=', '')
print(video_id)

transcript = YouTubeTranscriptApi.get_transcript(video_id)

output=''
for x in transcript:
  sentence = x['text']
  output += f' {sentence}\n'
print(output)

response = client.chat.completions.create(
  model="nvidia/llama-3.1-nemotron-70b-instruct",
  messages=[
    {"role": "system", "content": "You are a summarizer."},
    {"role": "assistant", "content": "access youtube videos and scrape the transcript from them and provide a summary of the video"},
    {"role": "user", "content": output}
  ]
)

summary = response.choices[0].message.content

response = client.chat.completions.create(
  model="nvidia/llama-3.1-nemotron-70b-instruct",
  messages=[
    {"role": "system", "content": "You are a summarizer."},
    {"role": "assistant", "content": "output a list of tags for this video in a python list such as ['item1', 'item2','item3']"},
    {"role": "user", "content": output}
  ]
)
tag = response.choices[0].message.content

print('>>>SUMMARY:')
print(summary)
print('>>>TAGS:')
print(tag)
print('>>>OUTPUT:')
#print(output)

#print(transcript)
