# Mock classes to simulate the structure of the OpenAI response
class MockChatCompletionMessage:
    def __init__(self, content, role='assistant'):
        self.content = content
        self.role = role

class MockChoice:
    def __init__(self, message, finish_reason='stop', index=0):
        self.message = message
        self.finish_reason = finish_reason
        self.index = index

class MockCompletionUsage:
    def __init__(self, completion_tokens, prompt_tokens, total_tokens):
        self.completion_tokens = completion_tokens
        self.prompt_tokens = prompt_tokens
        self.total_tokens = total_tokens

class MockChatCompletion:
    def __init__(self):
        self.id = 'chatcmpl-AOumIW7aoPueDmuMp1AyBS7glOjqt'
        self.created = 1730501490
        self.model = 'gpt-3.5-turbo-0125'
        self.object = 'chat.completion'
        self.choices = [
            MockChoice(
                message=MockChatCompletionMessage(
                    content="""1. Which Apple products are you interested in learning more about?
   - iPhone
   - iPad
   - Mac
   - MacBook Pro
   - Mac mini
   - iMac
   - AirPods Pro

2. Are you looking for information on software updates or new product releases?
   - Updates
   - New products
   - Both

3. Are you interested in Apple Intelligence or AI features?
   - Yes
   - No
   - Maybe

4. Do you have an iPhone 12 or higher that you are willing to trade in for credit?
   - Yes
   - No
   - I don't own one

5. Are you interested in Apple Card and its cash back rewards?
   - Yes
   - No
   - Maybe

6. Are you a fan of Apple TV+ or any specific content on it like FAM Gallery or NBA 2K25?
   - Yes
   - No
   - I haven't watched it"""
                )
            )
        ]
        self.usage = MockCompletionUsage(completion_tokens=204, prompt_tokens=317, total_tokens=521)
