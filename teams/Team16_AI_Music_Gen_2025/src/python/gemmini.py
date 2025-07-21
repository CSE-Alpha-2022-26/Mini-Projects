import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def gemmini_prompt(prompt):
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""CONTEXT: You are a prompt generator.You are given key words for a music prompt enclosed within input tags, with which you are to create a prompt intended for an AI music generation tool. You are to write the prompt in a way similar to how the prompts given below are structured and styled as that's how the model prefers the output to be.The prompt must include all the keywords and you can also assume additional information based on the keywords you get.

INSTRUCTION:
- Give output of prompt enclosed within input tags in the styles shown, be creative and add information where and if needed.Input tags are not needed in the output.
-  keep note progressions, tempo as any of [Slow (relaxed), Moderate (balanced), Fast (energetic) --  USE THE EXACT WORD AS IN THIS LIST FOR TEMPO] and other such useful info. 
- Be detailed, descriptive and useful (2-3 lines).
- ONLY RETURN THE NEW PROMPT AS TEXT, NO OTHER TEXT SHOULD BE PRESENT IN YOUR REPLY.

<input>
{prompt}
</input>

Expected output:

A melodic electronic composition with classical influences, featuring a string ensemble, trumpet, brass section, synth strings, and drums. Set in F# minor with a 4/4 time signature, it moves at an Allegro tempo. The mood evokes a cinematic, spacious, and epic atmosphere while maintaining a sense of relaxation. Slow (relaxed).


A classical piece that could be part of a film soundtrack, this composition is a soothing blend of acoustic guitar, flute, clarinet, oboe, and contrabass. With a tempo of 115 beats per minute, it's set in the key of E minor and maintains a 4/4 time signature throughout. The chord progression of Em, D, Dm, A, and Am adds to its emotional and romantic ambiance, making it an ideal choice for a relaxing listening experience. Moderate (balanced).

A melodic and happy pop song with classical influences, featuring a piano as the sole instrument. Set in the key of G# minor with a 4/4 time signature, it maintains a Moderato tempo throughout. The chord progression of Ebm, B, C#, Ebm, and B recurs frequently, lending a sense of familiarity to the piece. Fast (energetic).

"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.5,
        max_output_tokens=1000,
        response_mime_type="text/plain",
    )
    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        output += chunk.text  # accumulate chunks into one string

    return output.strip()  # return final result with whitespace trimmed


if __name__ == "__main__":
    input_prompt = "An instrumental piece featuring a solo Piano in A Major with a Classical genre. Allegro tempo with expressive dynamics. Follows notes in the order: d#3 e3 a#2 a2 c#3 d3 c3 b2 a2 b2 Emphasize harmonic texture over rhythmic complexity."

    out = gemmini_prompt(input_prompt)
    print(out)