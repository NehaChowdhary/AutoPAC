import pandas as pd
import sys

def separate_comments_from_code(code_with_comments):
    code_comment_dict = {}
    current_comment = None

    for line in code_with_comments.split('\n'):
        line = line.strip()
        if line.startswith('#'):
            current_comment = line
            code_comment_dict[current_comment] = []
        elif current_comment is not None:
            code_comment_dict[current_comment].append(line)

    return code_comment_dict

if __name__ == '__main__':
    code_with_comments = ""

    try :
        if(len(sys.argv)<=1):
            raise BaseException("Filepath not provided!")

        if(len(sys.argv)<=2):
            raise BaseException("Output file name not provided!")

        filepath = sys.argv[1]
        output_file=sys.argv[2]

        with open(filepath,'r') as fobj:
            code_with_comments = fobj.read()

        code_with_dict = separate_comments_from_code(code_with_comments)

        # Convert dictionary to DataFrame
        df = pd.DataFrame(columns=['question', 'answer'])
        for comment, codes in code_with_dict.items():
            for code in codes:
                df = df._append({'question': comment, 'answer': code if code.strip() else ''}, ignore_index=True)

        '''
            Data preprocessing
        '''

        # Dataframe drop null values
        df.dropna(inplace=True)

        # Group similar lines together
        df = df.groupby('question')['answer'].apply(lambda x: ' \n'.join(x)).reset_index()

        # Replace # in question by null
        df['question'] = df['question'].str.replace('# ', '')
        df['answer'].replace('', 'null', inplace=True)

        # Filter out rows where the question has only one word
        df = df[df['question'].str.split().str.len() > 1]
        df = df[df['answer']!="null"]

        print("Dataframe: \n",df)

        output_file_name = sys.argv[2]
        df.to_csv(output_file_name,index=False)
    except BaseException as be:
        print(be)


# Filter rows where the second column is not "null"
filtered_df = df[~(df.iloc[:, 1].str.strip().isin(['', '  ']))]

# Store the filtered DataFrame in a new CSV file
filtered_df.to_csv(output_file, index=False)

print("Filtered DataFrame saved to", output_file)







