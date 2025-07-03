#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from crews.meeting_minutes_crew.meeting_minutes_crew import MeetingMinutesCrew
from openai import OpenAI
from pydub import AudioSegment
from pydub.utils import make_chunks
from pathlib import Path
from dotenv import load_dotenv
import agentops
import os


load_dotenv()
client = OpenAI()

class MeetingMinutesState(BaseModel):
    transcript: str = ""
    meeting_minutes: str = ""


class MeetingMinutesFlow(Flow[MeetingMinutesState]):

    @start()
    def transcribe_meeting(self):
        print("Generating transcription")
        SCRIPT_DIR = Path(__file__).parent
        audio_path = str(SCRIPT_DIR / "EarningsCall.wav")
        
        # Load the audio file
        audio = AudioSegment.from_file(audio_path, format="wav")
        
        # Define chunk length in milliseconds (e.g., 1 minute = 60,000 ms)
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)

        # Transcribe each chunk
        full_transcription = ""
        for i, chunk in enumerate(chunks):
            print(f"Transcribing chunk {i+1}/{len(chunks)}")
            chunk_path = f"chunk_{i}.wav"
            chunk.export(chunk_path, format="wav")
            
            with open(chunk_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                full_transcription += transcription.text + " "

        self.state.transcript = full_transcription
        print(f"Transcription: {self.state.transcript}")
        
    @listen(transcribe_meeting)
    def generate_meeting_minutes(self):
        print("Generating Meeting Minutes")
        crew = MeetingMinutesCrew()
        inputs = {
            "transcript": self.state.transcript
        }
        meeting_minutes = crew.crew().kickoff(inputs)
        self.state.meeting_minutes = meeting_minutes
    
    
def kickoff():
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = "<your_openai_api_key>"

    AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY") or '8094894f-32a3-4862-a367-74860171f9b6'
    agentops.init(
        api_key=AGENTOPS_API_KEY,
        default_tags=['crewai']
    )
    # session = agentops.init(api_keys=os.getenv("AGENTOPS_API_KEY"))
    meeting_minutes_flow = MeetingMinutesFlow()
    meeting_minutes_flow.kickoff()
    # session.end()


if __name__ == "__main__":
    kickoff()
