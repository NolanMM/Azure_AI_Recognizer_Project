from openai import OpenAI

api_key = "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"  # this is liams key (I paid for it as well since it was easier to test)
client = OpenAI(api_key=api_key)


def openAPIRequest(MCQ, TF, FB, WP, contextai):
    prompt = f"Create a mock exam/midterm given the review content context json. Each question in the mock exam must have its own context and not reference specific words or items in the context provided. This is the context: {str(contextai)}. "
    teacher_prompt = f"You are a professor/Teacher creating an exam/midterm. You have provided students with review content of the topics on the exam to help them study. Based on the review content, construct a mock exam to assist them further and include the anwser sheet at the very end of the mock exam generated. If math equations are needed write them in latex form for ease of use  The mock exam/midterm will have: {str(MCQ)} Multiple choice questions, {str(TF)} true or false questions, {str(FB)} fill in the blank questions and {str(WP)} word problem questions"
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": teacher_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    # Check if completion.choices is not empty and has a valid response
    if completion.choices and completion.choices[0].message.content:
        # Extract the mock exam from OpenAI's response
        mock_exam = completion.choices[0].message.content

        # Print the test in a format that is easy to read
        # print( mock_exam)

        # Return the mock exam as a dictionary
        return {"mock_exam": mock_exam}
    else:
        return {"error": "Empty or malformed response from OpenAI"}


def OpenAI_Module(contextai):
    # Input the percentages of each type of question
    MCQ = 5
    TF = 5
    FB = 5
    WP = 5

    # Call API request
    mock_exam_dict = openAPIRequest(MCQ, TF, FB, WP, contextai)

    # prints the response in the dictionary format
    # print(mock_exam_dict)

    return mock_exam_dict
