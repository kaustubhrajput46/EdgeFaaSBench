import speech_recognition as sr
import time as t

def handle(req):
    startTime = t.time()
    finalData = ''
    # List all files in a dictionary using OS.listdir
    filename = 'ENG_F.wav'
    try:
        # Initialize the recorder
        r = sr.Recognizer()
        # OPen the file
        with sr.AudioFile(filename) as source:
            # listen for data (load audio in memory)
            audio_data = r.listen(source)
            # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            finalData = r.recognize_google(audio_data)
            print("Converting audio transcripts into text ...")
            print("\nThis is the output:", finalData)
            # Saving the output to a text file and also print the output
            with open("output.txt", "w") as output:
                output.write(finalData)
                print("Data has been written to the file...")
    except Exception as e:
        print("Following error was obeserved:", e)
        print("Exiting the code.")
        exit(0)
    
    endTime = t.time()
        
    return "The function has executed successfully in {:.2f} seconds.".format(endTime-startTime)