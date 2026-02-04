
#____________________________________
#| IMPORTING THE PACKAGES/LIBRARIES |
#-----------------------------------|
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import wikipedia
import re
import pyjokes
import random
import sys
import requests
import webbrowser
import os
from googletrans import Translator
import mtranslate
import shutil
import subprocess



listener = sr.Recognizer()
engine = pyttsx3.init('sapi5')
translator = Translator()



#now I am changing voice properties
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)


#defining the talk function for my dodo

def talk(text):
    print('| DodoAI:', str(text))
     #  text = mtranslate.translate(text, to_language="ur", from_language="en-in")
  # print(text)
    engine.say(text)
    engine.runAndWait()
    print("                 ")
 
print(" ")
print("==========================================================","|          ====================================          |", "|          | DODO AI - YOUR ASSISTANT CHATBOT |          |", "|          ====================================          |","==========================================================", sep = "\n")
introtext = "Hello, I am Dodo AI. How can I help you?"
talk(introtext)



def take_command():
  command = ""
  try:
    with sr.Microphone() as source:
        print("_________________", "|   LISTENING   |", "-----------------", sep="\n")
        print("           ")
        # Calibrate for ambient noise to avoid instantaneous timeouts
        try:
            listener.adjust_for_ambient_noise(source, duration=0.8)
        except Exception:
            # Non-fatal; continue without calibration
            pass

        # Wait up to 5s for phrase to start, capture up to 8s of speech
        try:
            voice = listener.listen(source, timeout=15, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            raise

        # Recognize speech
        try:
            command = listener.recognize_google(voice, language='en-in')
        except sr.UnknownValueError:
            # Speech was unintelligible
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return ""

        # translation from urdu to english so that dodo can understand
        try:
            command = mtranslate.translate(command, to_language='en-in')
        except Exception:
            # If translation fails, continue with original text
            pass
        command = command.lower()
  except sr.WaitTimeoutError:
        print("No response within timeout.")
        talk("You were silent for too long. Try again.")
  except AssertionError as ae:
        print(f"Microphone not ready: {ae}")
        talk("Sorry, there was an issue accessing your microphone.")
  except Exception as e:
      print(f"Unexpected error in take_command: {e}")
      # avoid raising to keep loop running
      return ""
  return command



def run_dodo():
    command = take_command()
    print("| You:", command)







#____________________________________________
#| PART- ONE: THE INFORMATION/FACT SECTION: |
#-------------------------------------------|

    try:
     search_variations1 = ['what is a', 'what is the', 'who is', 'who is the', 'give info about', 'tell me something', 'how do', 'what do you know', 'what you know',
                          'can you tell me', 'could you tell me', 'can you please tell me about', 'could you please tell me about',
                          'who was', 'what happened',  'what are the','what were the', 'tell me about', 'tell me more about', 'how do', 'describe', 'description of'
                           'why did the', 'give me details about', 'what happened to', 'can you explain', 'could you explain', 'can you please explain',
                           'could you please explain', 'what does', 'what is the meaning of',  'is there any',  'how can i find', 'what do you mean by',
                           'how would you describe', 'why did', 'how did']
     for search in search_variations1:
         if search in command and 'google' not in command and 'your' not in command and 'date today' not in command:
             thingtosearch = command.replace(search, '')
             info = wikipedia.summary(thingtosearch, 2)
             talk(info)
             break
    except:
      talk("I am really Sorry, I couldn't find anything related to your question.")


    try:
     search_variations2 = ['where is', 'where is the']
     for search in search_variations2:
         if search in command:
             thingtosearch = command.replace(search, '')
             info = wikipedia.summary(thingtosearch, 1)
             talk(info)
             break
    except:
      talk("I am really Sorry, I couldn't find anything related to your question.")


    try:
     search_variations3 = ['who made', 'who invented', 'who presented', 'what is the meaning of']
     for search in search_variations3:
         if search in command:
             info = wikipedia.summary(command,2)
             talk(info)
    except:
      talk("I am really Sorry, I couldn't find your info.")

    try:
     search_variations4 = ['how to', 'when did', 'how can', 'how does', 'why is', 'why does', 'when was', 'how might', 'what caused']
     for search in search_variations4:
         if search in command:
             info = wikipedia.summary(command,2)
             talk(info)
    except:
      talk("I am really Sorry, I couldn't find your info.")

    if 'how do airplanes fly' in command:
        text = 'Airplanes fly due to the lift generated by their wings, which is a result of air pressure differences.'
        print(text)
        talk(text)



#_____________________________________
#| PART- TWO: DATE, TIME, & WEATHER: |
#------------------------------------|

    if 'what time is it' in command or 'what time it is' in command or 'what time now' in command:
         time = datetime.datetime.now().strftime('%I:%M %p')
         talk('Current time is: ' + time)

    elif 'what date' in command or 'what is the date today' in command or 'what day it is' in command or 'what date it is' in command:
        date = datetime.datetime.now().strftime('%A, %d %B %Y')
        talk(f"Today's date is: {date}")

    elif ('weather' in command or 'temperature' in command) and 'in' in command:
        def get_weather(city):
            api_key = 'ea05112c7d79499fa89135627242312'
            url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}'
            try:
                response = requests.get(url)
                weather = response.json()
                
                if 'current' in weather:
                    temperature = weather['current']['temp_c']
                    description = weather['current']['condition']['text']
                    talk(f"The current temperature in {city} is {temperature}°C and the weather is {description}.")
                else:
                    talk(f"Sorry, I couldn't find the weather information for {city}.")
            except:
                talk("Sorry, I couldn't fetch the weather data at the moment.")

        city = command.split('in')[-1].strip()  
        weather_info = get_weather(city)


#__________________________________
#| PART- FOUR: MAKING A SCHEDULE: |
#---------------------------------|

  #  elif 'add tasks' in command or 'i have to do' in command:
   #     task = command.replace('add tasks' or 'i have to do', "").strip()
    #    if task != "":\
     #       with open('todo.txt', 'a') as file:
      #      file.write(task, "")


#_________________________________
#| PART- TWO: THE GOOGLE SEARCH: |
#--------------------------------|
    try:
     google_search_variations = ['google', 'google it', 'google this', 'google that']
     for variation in google_search_variations:
        if variation in command:
            search = command.replace(variation, '').strip()
            talk(f"Googling: {search}")
            pywhatkit.search(search)
            break
    except:
       talk("Try again, please.")
            



#_________________________________
#| PART- THRE: OPEN A WEBSITE: |
#--------------------------------|
    try:
     open_app_variations = ['open', 'open the app', 'open the website']
     for variation in open_app_variations:
        if variation in command:
            search = command.replace(variation, '').strip()
            search2 = "https://"+search
            talk(f"Opening: {search2}")
            pywhatkit.search(search2)
            break
    except:
       talk("Try again, please.")
            


#________________________________________
#| PART- THREE: THE DEFINITION SECTION: |
#---------------------------------------|
    science_definitions = {
        "Science": "Science is the systematic study of the structure and behavior of the physical and natural world through observation and experiment. It encompasses fields like biology, chemistry, physics, and earth sciences.",
        "Physics": "Physics is the branch of science concerned with the nature and properties of matter and energy. It seeks to understand the fundamental forces of the universe and the behavior of matter and energy in space and time.",
        "Chemistry": "Chemistry is the scientific study of the properties, composition, and behavior of matter. It involves understanding how substances interact, combine, and change to form new substances.",
        "Biology": "Biology is the study of living organisms, their structure, function, growth, origin, evolution, and distribution. It covers areas like genetics, ecology, and physiology.",
        "Mathematics": "Mathematics is the abstract science of number, quantity, and space, either as abstract concepts (pure mathematics), or as applied to other disciplines such as physics and engineering (applied mathematics).",
        "Geology": "Geology is the study of the Earth's physical structure, its history, and the processes that shape it. It involves understanding the Earth's materials, such as rocks and minerals, and how they change over time.",
        "Astronomy": "Astronomy is the scientific study of celestial objects, space, and the universe as a whole. It deals with the positions, motions, and properties of objects in space.",
        "Psychology": "Psychology is the scientific study of behavior and mental processes, including how individuals think, feel, and act. It also explores how mental health and cognitive functions affect human behavior.",
        "Sociology": "Sociology is the study of society and social behavior. It focuses on the structure of social groups, institutions, and the interactions between individuals within a society.",
        "Anthropology": "Anthropology is the study of humans, their societies, cultures, and biological aspects. It includes subfields like cultural anthropology, archaeology, and physical anthropology.",
        "Philosophy": "Philosophy is the study of fundamental questions regarding existence, knowledge, values, reason, mind, and language. It involves critical thinking and reasoning about life's essential questions.",
        "Economics": "Economics is the study of the production, distribution, and consumption of goods and services. It looks at how individuals, businesses, and governments make choices about resource allocation.",
        "Political Science": "Political science is the study of government systems, political behavior, and the analysis of political activities, political thoughts, and political entities.",
        "Education": "Education is the process of acquiring knowledge, skills, values, and habits through teaching, learning, and study. It can occur in formal institutions like schools or informally through personal experience.",
        "Law": "Law is the system of rules that a particular country or community recognizes as regulating the actions of its members. It includes the study of legal systems, civil rights, and the application of justice.",
        "History": "History is the study of past events, particularly in human affairs. It seeks to understand the events, individuals, and movements that have shaped the world as we know it today.",
        "Linguistics": "Linguistics is the scientific study of language, including its structure, sounds (phonology), meaning (semantics), grammar, and the ways in which languages evolve and interact.",
        "Engineering": "Engineering is the application of scientific principles to design, build, and maintain structures, machines, and systems. It involves various branches such as mechanical, electrical, civil, and computer engineering.",
        "Medicine": "Medicine is the science and practice of diagnosing, treating, and preventing diseases and injuries. It involves the study of the human body, its functions, and various medical interventions.",
        "Agriculture": "Agriculture is the science, art, and practice of cultivating soil, growing crops, and raising animals for food, fiber, medicinal plants, and other products used to sustain and enhance human life.",
        "Environmental Science": "Environmental science is the study of the environment and the interactions between humans and nature. It focuses on solving environmental issues such as pollution, conservation, and climate change.",
        "Ecology": "Ecology is the branch of biology that deals with the interactions between organisms and their environment. It focuses on ecosystems, biodiversity, and the balance of nature.",
        "Genetics": "Genetics is the study of heredity and the variation of inherited characteristics. It involves understanding how traits are passed from one generation to the next through genes.",
        "Botany": "Botany is the scientific study of plants, including their physiology, structure, genetics, ecology, and evolution. It also includes the classification and use of plants.",
        "Zoology": "Zoology is the scientific study of animals, including their biology, behavior, and interactions with their environments. It covers both living animals and their evolutionary history.",
        "Microbiology": "Microbiology is the study of microscopic organisms, such as bacteria, viruses, fungi, and protozoa. It involves understanding their structure, function, and impact on humans, animals, and the environment.",
        "Biochemistry": "Biochemistry is the study of the chemical processes within and related to living organisms. It deals with the structure and function of biomolecules like proteins, lipids, and nucleic acids.",
        "Physiology": "Physiology is the study of the functions and mechanisms in living systems. It includes how organs and systems in the body work together to maintain life and health.",
        "Chemistry of Life": "Chemistry of life, also known as biochemistry, is the study of the chemical processes and substances that occur within living organisms, such as enzymes, DNA, and metabolic pathways.",
        "Cell Biology": "Cell biology is the study of cells, their structure, function, and behavior. It focuses on how cells carry out their functions and interact with each other in multicellular organisms.",
        "Neuroscience": "Neuroscience is the scientific study of the nervous system, including the brain, spinal cord, and neural networks. It explores how the brain controls behavior, thoughts, and emotions.",
        "Astrophysics": "Astrophysics is a branch of astronomy that focuses on the physical properties and behavior of celestial bodies and the universe as a whole, using principles of physics and mathematics.",
        "Thermodynamics": "Thermodynamics is the branch of physics concerned with heat and temperature and their relation to energy and work. It involves laws that govern energy flow and conversion.",
        "Acoustics": "Acoustics is the study of sound, its production, transmission, and effects. It involves both physical properties of sound waves and their psychological perception.",
        "Optics": "Optics is the study of light and its interactions with matter, including the behavior of lenses, mirrors, and optical systems in devices like telescopes and microscopes.",
        "Biophysics": "Biophysics is an interdisciplinary science that applies the principles and methods of physics to understand biological systems and processes, such as protein folding and neural activity.",
        "Seismology": "Seismology is the study of seismic waves that travel through the Earth's interior, providing insights into the Earth's structure and the causes of earthquakes.",
        "Meteorology": "Meteorology is the science of the atmosphere and weather, focusing on the study of climate patterns, weather systems, and forecasting techniques.",
        "Oceanography": "Oceanography is the study of the Earth's oceans, including their physical properties, chemical composition, biological organisms, and ecosystems.",
        "Quantum Mechanics": "Quantum mechanics is a fundamental theory in physics describing the behavior of matter and energy at very small scales, such as atoms and subatomic particles, where classical mechanics no longer applies.",
        "Relativity": "Relativity refers to the theories of space and time developed by Albert Einstein, including special and general relativity, which revolutionized our understanding of gravity and the universe's structure.",
        "Solid State Physics": "Solid-state physics is the branch of physics that deals with the properties and behavior of solid materials, particularly in the areas of electronics, magnetism, and crystallography.",
        "Nuclear Physics": "Nuclear physics is the branch of physics concerned with the structure, behavior, and interactions of atomic nuclei, including reactions like fission and fusion.",
        "Chemical Engineering": "Chemical engineering is the branch of engineering that applies principles of chemistry, physics, biology, and mathematics to design, operate, and optimize chemical processes and production systems.",
        "Agronomy": "Agronomy is the science and technology of producing and using plants for food, fuel, fiber, and land reclamation. It involves the study of crop production, soil management, and the impact of environmental factors on agricultural practices.",
        "Veterinary Science": "Veterinary science is the branch of science that deals with the prevention, diagnosis, and treatment of diseases in animals. It includes various specialties like surgery, pharmacology, and animal behavior.",
        "Toxicology": "Toxicology is the study of the harmful effects of chemicals, substances, and environmental factors on living organisms. It focuses on how poisons and toxins affect the body and the environment.",
        "Paleontology": "Paleontology is the scientific study of the history of life on Earth through the examination of plant and animal fossils. It provides insight into evolutionary processes and ancient ecosystems.",
        "Genomics": "Genomics is the study of genomes, the complete set of genetic material in an organism. It involves analyzing the structure, function, evolution, and mapping of genes.",
        "Bioinformatics": "Bioinformatics is the application of computational techniques to analyze and interpret biological data, particularly genetic and genomic information. It combines biology, computer science, and information technology.",
        "Pharmacology": "Pharmacology is the study of drugs and their interactions with living systems. It involves understanding how drugs affect the body and how the body processes drugs to treat diseases and improve health.",
        "Materials Science": "Materials science is the study of the properties, structure, and behavior of materials. It involves understanding how materials like metals, polymers, and ceramics are used in engineering and technology.",
        "Cognitive Science": "Cognitive science is the interdisciplinary study of mind and intelligence, encompassing fields like psychology, neuroscience, philosophy, linguistics, and artificial intelligence. It focuses on how humans and machines process information.",
        "Hematology": "Hematology is the branch of medicine that deals with the study of blood, blood-forming organs, and blood diseases. It focuses on conditions like anemia, leukemia, and clotting disorders.",
        "Immunology": "Immunology is the study of the immune system, including how the body defends itself against infections, diseases, and foreign substances. It covers topics like antibodies, vaccines, and autoimmune diseases.",
        "Astrobiology": "Astrobiology is the study of the origin, evolution, and distribution of life in the universe. It involves searching for extraterrestrial life and understanding the conditions necessary for life to exist elsewhere.",
        "Linguistic Anthropology": "Linguistic anthropology is the study of language in its social and cultural context. It explores how language shapes human behavior, identity, and societal structures.",
        "Forensic Science": "Forensic science applies scientific methods and principles to solve crimes and legal issues. It includes fields like DNA analysis, toxicology, and forensic pathology.",
        "Environmental Engineering": "Environmental engineering is the application of engineering principles to improve the environment. It focuses on issues like pollution control, waste management, and sustainable development.",
        "Health Science": "Health science is the multidisciplinary field that focuses on the study of health, healthcare, and medical practices. It includes fields like public health, medical research, and nursing.",
        "Nephrology": "Nephrology is the branch of medicine that deals with the study of kidney function, diseases, and treatments. It includes the diagnosis and management of conditions like kidney failure and dialysis.",
        "Endocrinology": "Endocrinology is the study of hormones and their effects on the body. It involves understanding how the endocrine system regulates processes like metabolism, growth, and reproduction.",
        "Speech Pathology": "Speech pathology is the study of speech and language disorders, including how to diagnose, treat, and manage conditions that affect communication, such as stuttering and speech impairments.",
        "Oceanography": "Oceanography is the study of the Earth's oceans, including their physical properties, chemical composition, biological organisms, and ecosystems. It also explores ocean currents and the impact of oceans on global climate.",
        "Cytology": "Cytology is the study of cells, particularly their structure, function, and behavior. It examines how cells interact with their environment and how cellular processes are regulated.",
        "Quantum Computing": "Quantum computing is a field of computing based on the principles of quantum mechanics. It aims to develop computers that can process information in ways that classical computers cannot, offering potential breakthroughs in various areas like cryptography and artificial intelligence.",
        "Nanotechnology": "Nanotechnology is the manipulation and application of matter at an atomic or molecular scale. It focuses on creating new materials and devices with unique properties that emerge at the nanoscale.",
        "Geophysics": "Geophysics is the study of the physical properties and behavior of the Earth using methods from physics. It includes the study of the Earth's magnetic field, gravitational field, seismic waves, and the internal structure of the Earth.",
        "Climatology": "Climatology is the study of climate, including long-term weather patterns, temperature, precipitation, and atmospheric phenomena. It is used to understand and predict changes in climate and its impact on the environment.",
        "Hydrology": "Hydrology is the study of water and its movement across the Earth. It involves understanding the distribution, circulation, and properties of water, including its interaction with the atmosphere, soil, and organisms.",
        "Botany": "Botany is the scientific study of plants, including their structure, function, growth, and classification. It also explores plant ecology, genetics, and their uses in agriculture and medicine.",
        "Soil Science": "Soil science is the study of soil as a natural resource, including its formation, classification, mapping, and fertility. It focuses on understanding soil properties to optimize agricultural production.",
        "Biomechanics": "Biomechanics is the study of the mechanical principles that govern the movements of living organisms. It includes understanding how muscles, bones, and joints work together to create movement.",
        "Philosophy of Science": "Philosophy of science is the study of the assumptions, foundations, and implications of scientific knowledge. It explores how science is conducted, its limitations, and its relationship with truth and reality.",
        "Cryogenics": "Cryogenics is the study of the production and effects of low temperatures, typically below -150°C. It involves understanding the behavior of materials at these temperatures and their applications in fields like medicine and space exploration.",
        "Ethology": "Ethology is the scientific study of animal behavior, particularly in natural environments. It involves understanding the biological, ecological, and evolutionary aspects of behavior.",
        "Mathematical Biology": "Mathematical biology applies mathematical models and techniques to understand biological systems and processes. It is used to study phenomena like population dynamics, disease spread, and genetics.",
        "Astrophysics": "Astrophysics is the branch of astronomy that applies the laws of physics to understand the nature and behavior of celestial objects and the universe. It includes the study of stars, galaxies, black holes, and cosmic phenomena.",
        "Biophysics": "Biophysics is the interdisciplinary field that applies principles and methods of physics to biological systems. It involves understanding how biological molecules interact and how energy flows in living organisms.",
        "Epidemiology": "Epidemiology is the study of the distribution and determinants of health-related events in populations. It focuses on understanding how diseases spread and how to control outbreaks.",
        "Sociology of Education": "Sociology of education is the study of how education impacts society and how societal factors influence educational systems and outcomes. It explores issues like inequality, educational access, and curriculum development.",
        "Cell Biology": "Cell biology is the branch of biology that studies the structure, function, and behavior of cells. It involves understanding the various organelles, cellular processes, and how cells interact with their environment.",
        "Genetics": "Genetics is the study of heredity and variation in organisms. It focuses on how traits are inherited, the role of genes in development and functioning, and how genetic disorders are passed from one generation to the next.",
        "Evolutionary Biology": "Evolutionary biology is the study of the processes that drive the evolution of species over time. It examines natural selection, genetic drift, mutations, and gene flow as mechanisms that shape the diversity of life.",
        "Ecology": "Ecology is the branch of biology that studies the interactions of organisms with their environment and each other. It focuses on ecosystems, food chains, biodiversity, and environmental impacts on species.",
        "Microbiology": "Microbiology is the study of microscopic organisms, including bacteria, viruses, fungi, and protozoa. It explores their structure, function, classification, and their role in disease, decomposition, and environmental cycles.",
        "Physiology": "Physiology is the study of the normal functions of living organisms and their parts. It explores how organs, tissues, and cells work together to maintain life processes like circulation, digestion, and respiration.",
        "Biochemistry": "Biochemistry is the study of the chemical processes and substances that occur within living organisms. It bridges biology and chemistry, focusing on the structure and function of molecules like proteins, lipids, and nucleic acids.",
        "Botany": "Botany is the branch of biology that studies plants, including their physiology, structure, growth, reproduction, and ecology. It covers areas like plant genetics, classification, and the role of plants in ecosystems.",
        "Zoology": "Zoology is the scientific study of animals, including their anatomy, physiology, behavior, classification, and ecology. It encompasses the study of all animal life, from insects to mammals.",
        "Immunology": "Immunology is the study of the immune system and its components, including the body's defense mechanisms against pathogens, such as bacteria, viruses, and fungi. It also involves understanding immune responses and diseases like autoimmune disorders.",
        "Molecular Biology": "Molecular biology focuses on the molecular mechanisms that govern biological processes. It includes the study of DNA, RNA, protein synthesis, and how molecular interactions control cell function and development.",
        "Developmental Biology": "Developmental biology studies the processes by which organisms grow and develop. It explores topics like cell differentiation, embryogenesis, and the genetic regulation of development.",
        "Neurobiology": "Neurobiology is the study of the nervous system and its components, including the brain, spinal cord, and peripheral nerves. It examines how nerve cells communicate and how the brain processes information.",
        "Endocrinology": "Endocrinology is the branch of biology that studies hormones and the endocrine system. It focuses on the regulation of biological functions such as metabolism, growth, reproduction, and stress responses.",

    #Definition of Physics Topics
        "Energy": "Energy is the capacity to do work. It can exist in various forms such as kinetic, potential, thermal, and electrical, and can be transformed from one form to another but is never created or destroyed, as per the law of conservation of energy.",
        "Force": "Force is a vector quantity that causes an object to undergo a change in motion. It is measured in newtons and is responsible for changes in velocity or the deformation of objects.",
        "Mass": "Mass is a measure of the amount of matter in an object. It is typically measured in kilograms and remains constant regardless of the object's location in the universe.",
        "Acceleration": "Acceleration is the rate of change of velocity of an object. It is measured in meters per second squared and can occur as a result of force applied to an object.",
        "Speed": "Speed is a scalar quantity that refers to how fast an object is moving. It is calculated as distance traveled divided by the time taken.",
        "Velocity": "Velocity is a vector quantity that specifies the speed and direction of an object's motion. It is the rate of change of position with respect to time.",
        "Momentum": "Momentum is the product of an object's mass and its velocity. It is a vector quantity and is conserved in isolated systems during collisions.",
        "Force of Friction": "The force of friction is the resistance encountered when two surfaces slide or try to slide across each other. It opposes the relative motion of the surfaces and depends on the nature of the surfaces in contact.",
        "Work": "Work is done when a force acts upon an object and causes it to move. It is calculated as the product of force and the distance moved in the direction of the force.",
        "Power": "Power is the rate at which work is done or energy is transferred. It is measured in watts (joules per second).",
        "Kinetic Energy": "Kinetic energy is the energy an object possesses due to its motion. It is calculated as one-half of the mass times the square of the velocity.",
        "Potential Energy": "Potential energy is the energy stored in an object due to its position or configuration. It is often associated with gravity, elastic deformation, or chemical bonds.",
        "Conservation of Energy": "The law of conservation of energy states that energy cannot be created or destroyed, only transformed from one form to another.",
        "Gravitational Force": "Gravitational force is an attractive force that acts between any two masses. It is described by Newton's law of universal gravitation and is responsible for the weight of objects.",
        "Newton's First Law of Motion": "Newton's first law, also known as the law of inertia, states that an object will remain at rest or in uniform motion unless acted upon by an external force.",
        "Newton's Second Law of Motion": "Newton's second law states that the acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass.",
        "Newton's Third Law of Motion": "Newton's third law states that for every action, there is an equal and opposite reaction.",
        "Centripetal Force": "Centripetal force is the force that acts on an object moving in a circular path, directed toward the center of the circle or axis of rotation.",
        "Work-Energy Theorem": "The work-energy theorem states that the work done on an object is equal to the change in its kinetic energy.",
        "Impulse": "Impulse is the product of the force acting on an object and the time it acts. It is also equal to the change in momentum of the object.",
        "Simple Harmonic Motion": "Simple harmonic motion is a type of periodic motion in which an object moves back and forth around a central equilibrium position. The motion is sinusoidal in nature and characterized by a restoring force proportional to displacement.",
        "Elastic Collision": "An elastic collision is one in which both momentum and kinetic energy are conserved. In such collisions, objects bounce off each other without deformation.",
        "Inelastic Collision": "An inelastic collision is one in which momentum is conserved, but kinetic energy is not. Some of the kinetic energy is converted into other forms of energy, like heat or sound.",
        "Circular Motion": "Circular motion refers to the motion of an object along a circular path. It can be uniform, where the object's speed is constant, or non-uniform, where the speed changes.",
        "Rotational Motion": "Rotational motion is the motion of an object that rotates around an axis. It involves angular displacement, velocity, and acceleration.",
        "Moment of Inertia": "The moment of inertia is a property of a body that determines its resistance to rotational motion. It depends on the mass distribution relative to the axis of rotation.",
        "Angular Momentum": "Angular momentum is the rotational analog of linear momentum. It is conserved in the absence of external torque and is given by the product of moment of inertia and angular velocity.",
        "Torque": "Torque is a measure of the rotational force applied to an object. It is calculated as the force multiplied by the perpendicular distance from the axis of rotation.",
        "Gravity": "Gravity is the force of attraction that pulls objects toward the center of the Earth. It is responsible for the weight of objects and governs the motion of planets and moons.",
        "Pressure": "Pressure is the force applied per unit area of surface. It is measured in pascals (Pa) and is a key concept in fluid mechanics.",
        "Density": "Density is the mass of an object per unit volume. It is a property that determines whether an object will float or sink in a fluid.",
        "Temperature": "Temperature is a measure of the average kinetic energy of the particles in a substance. It is usually measured in Celsius, Kelvin, or Fahrenheit.",
        "Heat": "Heat is the transfer of energy from a hotter object to a cooler one due to a difference in temperature. It can be transferred through conduction, convection, or radiation.",
        "Specific Heat Capacity": "Specific heat capacity is the amount of heat required to raise the temperature of a unit mass of a substance by one degree Celsius.",
        "Thermodynamics": "Thermodynamics is the branch of physics concerned with heat, work, and the energy transformations between them. It involves laws such as the conservation of energy and the increase of entropy.",
        "First Law of Thermodynamics": "The first law of thermodynamics, also known as the law of energy conservation, states that energy cannot be created or destroyed, only transferred or converted from one form to another.",
        "Second Law of Thermodynamics": "The second law of thermodynamics states that the total entropy of an isolated system always increases over time, and energy spontaneously tends to disperse.",
        "Third Law of Thermodynamics": "The third law of thermodynamics states that the entropy of a system approaches a constant minimum as the temperature approaches absolute zero.",
        "Entropy": "Entropy is a measure of the disorder or randomness in a system. In thermodynamics, it is often associated with the irreversibility of natural processes.",
        "Heat Engine": "A heat engine is a device that converts heat energy into mechanical work. It operates on the principles of thermodynamics, typically by transferring heat from a hot source to a cold sink.",
        "Ideal Gas": "An ideal gas is a theoretical gas whose behavior is described by the ideal gas law, where the gas particles do not interact and occupy no volume.",
        "Real Gas": "A real gas is a gas that does not behave according to the ideal gas law at high pressure or low temperature due to intermolecular forces and the finite volume of gas molecules.",
        "Electricity": "Electricity is the set of physical phenomena associated with the presence and motion of electric charge. It includes concepts like voltage, current, and resistance.",
        "Voltage": "Voltage, also known as electric potential difference, is the difference in electric potential energy between two points in an electric circuit. It is measured in volts.",
        "Current": "Electric current is the flow of electric charge through a conductor, usually in the form of electrons. It is measured in amperes.",
        "Resistance": "Resistance is the opposition to the flow of electric current. It is measured in ohms and depends on the material, length, and cross-sectional area of the conductor.",
        "Ohm's Law": "Ohm's law states that the current through a conductor is directly proportional to the voltage across it and inversely proportional to the resistance.",
        "Capacitor": "A capacitor is an electrical component that stores energy in the form of an electric field. It is used to store charge and release it when needed in a circuit.",
        "Inductor": "An inductor is a passive electronic component that resists changes in current. It stores energy in a magnetic field when current passes through it.",
        "Magnetic Field": "A magnetic field is a vector field surrounding magnetic materials and electric currents that exerts force on other magnetic materials and moving charges.",
        "Electromagnetic Wave": "An electromagnetic wave is a wave of oscillating electric and magnetic fields that propagates through space. It includes light, radio waves, and X-rays.",
        "Light": "Light is electromagnetic radiation that can be perceived by the human eye. It has properties of both waves and particles, and it travels at a speed of approximately 299,792 kilometers per second in a vacuum.",
        "Reflection": "Reflection is the change in direction of a wave when it bounces off a surface. The angle of incidence is equal to the angle of reflection.",
        "Refraction": "Refraction is the bending of light or any wave as it passes from one medium to another with a different refractive index, causing a change in the wave's speed and direction.",
        "Diffraction": "Diffraction is the bending of waves around obstacles or the spreading of waves when they pass through small openings. It is most noticeable with light and sound waves.",
        "Interference": "Interference is the process by which two or more waves superpose to form a resultant wave. It can be constructive (amplitudes add) or destructive (amplitudes cancel).",
        "Wave-Particle Duality": "Wave-particle duality is the concept that every particle or quantum entity can exhibit both wave-like and particle-like properties, as demonstrated in phenomena such as the double-slit experiment.",
        "Photoelectric Effect": "The photoelectric effect is the emission of electrons from a material when it absorbs electromagnetic radiation, particularly light. It provides evidence of the particle nature of light.",
        "Coulomb's Law": "Coulomb's law describes the force between two electric charges. The force is proportional to the product of the charges and inversely proportional to the square of the distance between them.",
        "Electric Field": "An electric field is a region around a charged particle within which a force would be exerted on other charged particles. It is represented by electric field lines that point from positive to negative charges.",
        "Magnetic Field": "A magnetic field is a field that surrounds magnetic materials and moving electric charges, influencing other moving charges or magnetic materials within the field.",
        "Faraday's Law of Induction": "Faraday's law of induction states that a change in magnetic flux through a coil of wire induces an electromotive force (EMF) in the coil, which can generate an electric current.",
        "Lenz's Law": "Lenz's law states that the direction of the induced current in a conductor due to a changing magnetic field will be such that it opposes the change in magnetic flux.",
        "Faraday's Constant": "Faraday's constant is the charge of one mole of electrons, approximately 96,485 coulombs. It relates the amount of electric charge to the amount of substance involved in electrochemical reactions.",
        "Electromagnetic Spectrum": "The electromagnetic spectrum is the range of all possible frequencies of electromagnetic radiation, including radio waves, microwaves, infrared, visible light, ultraviolet, X-rays, and gamma rays.",
        "Radio Waves": "Radio waves are a type of electromagnetic wave with the longest wavelengths and lowest frequencies. They are used for communication and broadcasting.",
        "Microwaves": "Microwaves are electromagnetic waves with shorter wavelengths than radio waves but longer than infrared. They are used in radar, satellite communication, and microwave ovens.",
        "Infrared Radiation": "Infrared radiation is electromagnetic radiation with wavelengths longer than visible light but shorter than microwaves. It is commonly associated with heat.",
        "Visible Light": "Visible light is the portion of the electromagnetic spectrum that can be detected by the human eye, with wavelengths between 400 nm and 700 nm.",
        "Ultraviolet Radiation": "Ultraviolet radiation is electromagnetic radiation with wavelengths shorter than visible light but longer than X-rays. It can cause sunburn and is used in sterilization.",
        "X-rays": "X-rays are high-energy electromagnetic waves with very short wavelengths. They are used in medical imaging and can penetrate various materials.",
        "Gamma Rays": "Gamma rays are the highest-energy form of electromagnetic radiation, with very short wavelengths. They are produced by nuclear reactions and are used in cancer treatment and sterilization.",
        "Thermal Conductivity": "Thermal conductivity is a property of a material that describes its ability to conduct heat. It measures how efficiently heat is transferred through a substance.",
        "Latent Heat": "Latent heat is the heat required to change the state of a substance without changing its temperature, such as melting or boiling.",
        "Specific Latent Heat": "Specific latent heat is the amount of heat required to change the state of one kilogram of a substance without changing its temperature.",
        "Brownian Motion": "Brownian motion is the random motion of particles suspended in a fluid, resulting from collisions with fast-moving molecules in the fluid.",
        "Doppler Effect": "The Doppler effect is the change in frequency or wavelength of a wave in relation to an observer moving relative to the source of the wave. It is observed in sound and light waves.",
        "Superconductivity": "Superconductivity is a phenomenon where certain materials, at very low temperatures, exhibit zero electrical resistance and the expulsion of magnetic fields.",
        "Conductors": "Conductors are materials that allow the easy flow of electric current due to the presence of free electrons. Examples include metals like copper and aluminum.",
        "Insulators": "Insulators are materials that do not allow the easy flow of electric current. Examples include rubber, plastic, and glass.",
        "Semiconductors": "Semiconductors are materials with electrical conductivity between that of conductors and insulators. They are used in electronic devices such as transistors and diodes.",
        "Ohm": "The ohm is the unit of electrical resistance, defined as the resistance between two points when one volt causes a current of one ampere.",
        "Electric Potential": "Electric potential is the amount of electric potential energy per unit charge at a point in space, measured in volts.",
        "Capacitance": "Capacitance is the ability of a body or system to store an electric charge. It is defined as the charge per unit voltage and is measured in farads.",
        "Inductance": "Inductance is the property of a conductor or circuit that opposes changes in current. It is measured in henries and is a key component in inductors.",
        "Magnetic Induction": "Magnetic induction is the process by which a material becomes magnetized when exposed to a magnetic field.",
        "Current Density": "Current density is the amount of electric current flowing through a unit area of a conductor. It is measured in amperes per square meter.",
        "Energy Density": "Energy density is the amount of energy stored in a given system or region of space per unit volume or mass.",
        "Potential Energy of an Electric Field": "Potential energy of an electric field refers to the energy stored within the field due to the positions of charges within it.",
        "Magnetic Moment": "Magnetic moment is a vector quantity that represents the strength and direction of a magnetic source, such as a magnet or a current loop.",
        "Resonance": "Resonance is the condition in which a system oscillates with greater amplitude at specific frequencies, known as resonant frequencies, due to the matching of the system's natural frequency with an external driving force.",
        "Conduction": "Conduction is the transfer of heat or electricity through a material without the movement of the material itself. It occurs due to the interactions between particles or electrons.",
        "Convection": "Convection is the process of heat transfer through the movement of fluids (liquids or gases), driven by differences in temperature and density within the fluid.",
        "Radiation": "Radiation is the transfer of heat in the form of electromagnetic waves, such as light or infrared radiation. It does not require a medium to travel.",
        "Wavefunction": "A wavefunction is a mathematical description of the quantum state of a system, representing the probabilities of the outcomes of measurements of physical quantities.",
        "Heisenberg Uncertainty Principle": "The Heisenberg uncertainty principle states that it is impossible to simultaneously measure the exact position and momentum of a particle with arbitrary precision.",
        "Schrodinger Equation": "The Schrodinger equation is a fundamental equation in quantum mechanics that describes how the quantum state of a system changes over time.",
        "Quantum Mechanics": "Quantum mechanics is the branch of physics that deals with the behavior of matter and energy on very small scales, such as atoms and subatomic particles.",
        "Wave-Function Collapse": "Wave-function collapse is the process by which a quantum system transitions from a superposition of states to a single, definite state upon measurement.",
        "Pauli Exclusion Principle": "The Pauli exclusion principle states that no two fermions (particles with half-integer spin) can occupy the same quantum state simultaneously.",
        "Fermion": "Fermions are particles that obey the Pauli exclusion principle and have half-integer spin. They include electrons, protons, and neutrons.",
        "Boson": "Bosons are particles that do not obey the Pauli exclusion principle and can occupy the same quantum state. They have integer spin and include photons, gluons, and the Higgs boson.",
        "Higgs Boson": "The Higgs boson is a particle associated with the Higgs field, which is believed to give other particles mass. Its discovery at CERN in 2012 confirmed the Higgs mechanism.",
        "String Theory": "String theory is a theoretical framework in which the fundamental particles are not point-like, but rather are one-dimensional 'strings' that vibrate at different frequencies.",
        "Dark Matter": "Dark matter is a form of matter that does not emit light or energy but exerts gravitational effects on visible matter. It is believed to make up a large portion of the universe's total mass.",
        "Dark Energy": "Dark energy is a mysterious form of energy that is thought to be responsible for the accelerated expansion of the universe. It accounts for about 68% of the universe's total energy content.",
        "Black Hole": "A black hole is a region of space where gravity is so strong that nothing, not even light, can escape from it. It forms when a massive star collapses under its own gravity.",
        "Singularity": "A singularity is a point in space where gravitational forces are so intense that spacetime becomes infinitely curved, and physical laws break down. This is believed to occur at the center of black holes.",
        "Event Horizon": "The event horizon is the boundary surrounding a black hole beyond which nothing, not even light, can escape. It marks the point of no return for objects falling into the black hole.",
        "Escape Velocity": "Escape velocity is the minimum speed an object must have in order to break free from the gravitational influence of a planet, star, or other celestial body.",
        "Cosmic Microwave Background": "The cosmic microwave background is the faint radiation left over from the Big Bang, providing important evidence for the origin and evolution of the universe.",
        "General Relativity": "General relativity is Einstein's theory of gravitation, which states that gravity is the result of the curvature of spacetime caused by the mass and energy of objects.",
        "Special Relativity": "Special relativity is Einstein's theory that describes the relationship between space and time for objects moving at constant speeds, particularly those moving near the speed of light.",
        "Spacetime": "Spacetime is the four-dimensional continuum combining the three dimensions of space and one of time, in which events occur and are measured.",
        "Quantum Entanglement": "Quantum entanglement is a phenomenon where two or more particles become correlated in such a way that the state of one particle instantaneously affects the state of the other, regardless of distance.",
        "Quantum Tunneling": "Quantum tunneling is the phenomenon where particles pass through a potential barrier that they classically should not be able to pass, due to their wave-like properties.",
        "Superposition Principle": "The superposition principle states that in a linear system, the net response at a given time or position is the sum of the individual responses from all independent influences.",
        "Antimatter": "Antimatter is composed of particles that are the opposites of the particles in ordinary matter, having opposite electric charges and quantum properties. When matter and antimatter meet, they annihilate each other.",
        "Neutron Star": "A neutron star is the collapsed core of a massive star that has exploded in a supernova. It is composed primarily of neutrons and has extremely high density and gravity.",
        "White Dwarf": "A white dwarf is a small, dense star that is the remnant of a medium or low-mass star that has exhausted its nuclear fuel. It is supported against collapse by electron degeneracy pressure.",
        "Red Giant": "A red giant is a large, luminous star in the late stages of its evolution, characterized by a red color due to its cooler surface temperature and the expansion of its outer layers.",
        "Solar Wind": "The solar wind is a stream of charged particles, primarily electrons and protons, that are emitted by the sun's outer layers and travel through the solar system.",
        "Solar System": "The solar system is the collection of the Sun and its orbiting planets, moons, asteroids, comets, and other objects, bound together by gravity.",
        "Orbit": "An orbit is the path that an object follows as it moves around another object in space, typically due to the gravitational attraction between the two.",
        "Kepler's Laws": "Kepler's laws describe the motion of planets in orbit around the Sun. These include the law of elliptical orbits, the law of equal areas, and the law of harmonies.",
        "Gravitational Waves": "Gravitational waves are ripples in spacetime caused by accelerated masses, such as merging black holes or neutron stars. They were first directly detected in 2015.",
        "Hubble's Law": "Hubble's law states that the velocity at which a galaxy is receding from an observer is directly proportional to its distance from the observer, providing evidence for the expanding universe.",
        "Big Bang Theory": "The Big Bang theory is the leading explanation for the origin of the universe, suggesting it began as an extremely hot, dense point approximately 13.8 billion years ago and has been expanding ever since.",
        "Dark Energy": "Dark energy is a form of energy that is thought to be responsible for the accelerated expansion of the universe, making up about 68% of the universe’s total energy density.",
        "Big Crunch": "The Big Crunch is a hypothetical scenario for the end of the universe in which it collapses back in on itself, due to the force of gravity overcoming the expansion of the universe.",
        "Big Freeze": "The Big Freeze is a possible fate of the universe where it continues to expand forever, causing it to gradually cool down and lose energy, eventually becoming dark and empty.",
        "Nuclear Fusion": "Nuclear fusion is the process by which two light atomic nuclei combine to form a heavier nucleus, releasing a significant amount of energy. It powers stars, including our Sun.",
        "Nuclear Fission": "Nuclear fission is the process by which a heavy atomic nucleus splits into two smaller nuclei, releasing a large amount of energy. It is used in nuclear power plants and atomic bombs.",
        "Fermi Paradox": "The Fermi paradox refers to the apparent contradiction between the high probability of extraterrestrial life in the universe and the lack of evidence or contact with such civilizations.",
        "Hawking Radiation": "Hawking radiation is the theoretical prediction that black holes emit radiation due to quantum effects near the event horizon, leading to the eventual evaporation of the black hole.",
        "Gravitational Lensing": "Gravitational lensing is the bending of light around a massive object, such as a galaxy or black hole, which acts like a lens, distorting and magnifying the light from objects behind it.",
        "Critical Mass": "Critical mass is the minimum amount of fissile material required to sustain a nuclear chain reaction. In a supercritical mass, the reaction will accelerate; in a subcritical mass, it will stop.",
        "Chain Reaction": "A chain reaction is a process where the products of one reaction initiate further reactions, such as in nuclear fission or chemical reactions.",
        "Tachyon": "A tachyon is a hypothetical particle that always moves faster than the speed of light. Its existence is not confirmed, but it is used in certain theoretical models of physics.",
        "Geosynchronous Orbit": "A geosynchronous orbit is an orbit around Earth where a satellite's orbital period matches the rotation period of Earth, allowing it to remain in the same position relative to the surface.",
        "Geostationary Orbit": "A geostationary orbit is a special case of geosynchronous orbit where a satellite's orbital period is 24 hours and its orbit is directly above the equator, appearing stationary relative to the Earth's surface.",
        "Escape Velocity": "Escape velocity is the minimum speed an object must reach to escape the gravitational pull of a celestial body without additional propulsion.",
        "Subatomic Particles": "Subatomic particles are particles smaller than an atom, including protons, neutrons, and electrons, as well as more exotic particles like quarks and neutrinos.",
        "Quarks": "Quarks are elementary particles that combine to form protons and neutrons. They come in six types: up, down, charm, strange, top, and bottom.",
        "Leptons": "Leptons are a class of elementary particles that include the electron, muon, tau, and their corresponding neutrinos. They do not undergo strong interactions.",
        "Quark-Gluon Plasma": "Quark-gluon plasma is a state of matter in which quarks and gluons, normally confined within protons and neutrons, exist freely. It is believed to have existed shortly after the Big Bang.",
        "Photons": "Photons are the elementary particles of light, which carry electromagnetic energy and have zero rest mass. They move at the speed of light.",
        "Neutrinos": "Neutrinos are very light, electrically neutral particles that interact only via the weak nuclear force and gravity. They are produced in nuclear reactions such as those in the Sun.",
        "Weak Nuclear Force": "The weak nuclear force is one of the four fundamental forces of nature, responsible for processes like beta decay, and it operates at very short distances.",
        "Strong Nuclear Force": "The strong nuclear force is the force that holds the nucleus of an atom together. It is the strongest of the four fundamental forces but operates only over very short distances.",
        "Electromagnetic Force": "The electromagnetic force is one of the fundamental forces, responsible for the interaction between charged particles. It governs phenomena like electricity, magnetism, and light.",
        "Gravitational Force": "Gravitational force is the force of attraction between two masses. It is one of the fundamental forces and operates over long distances, but is weaker than the other forces.",
        "Force of Friction": "The force of friction is the resistive force that opposes the relative motion of two surfaces in contact. It can be static (preventing motion) or kinetic (resisting motion).",
        "Elasticity": "Elasticity is the property of a material to return to its original shape and size after being deformed by an external force, such as stretching or compressing.",
        "Inertia": "Inertia is the property of an object to resist changes in its state of motion. An object at rest stays at rest, and an object in motion stays in motion unless acted upon by an external force.",
        "Angular Displacement": "Angular displacement is the angle through which an object rotates in a given time period, measured in radians.",
        "Angular Velocity": "Angular velocity is the rate at which an object changes its angular position, typically measured in radians per second.",
        "Angular Acceleration": "Angular acceleration is the rate at which an object's angular velocity changes with time, measured in radians per second squared.",
        "Moment of Inertia": "Moment of inertia is a measure of an object's resistance to changes in its rotational motion, analogous to mass in linear motion.",
        "Torque": "Torque is a measure of the rotational force applied to an object, calculated as the force multiplied by the distance from the pivot point.",
        "Centripetal Force": "Centripetal force is the force that acts on an object moving in a circular path, directed toward the center of the circle.",
        "Centrifugal Force": "Centrifugal force is an apparent force that acts outward on an object moving around a center, observed in a rotating reference frame.",
        "Rotational Kinetic Energy": "Rotational kinetic energy is the energy an object possesses due to its rotation, given by the formula 1/2 Iω², where I is the moment of inertia and ω is angular velocity.",
        "Uniform Circular Motion": "Uniform circular motion is the motion of an object traveling at a constant speed along a circular path, with constant angular velocity.",
        "Non-uniform Circular Motion": "Non-uniform circular motion is the motion of an object along a circular path with a changing speed or angular velocity.",
        "Angular Momentum": "Angular momentum is a measure of the rotational motion of an object, calculated as the product of its moment of inertia and angular velocity.",
        "Kepler's Laws of Planetary Motion": "Kepler's laws describe the motion of planets around the sun, including the law of ellipses, equal areas, and the harmonic law relating orbital period to distance.",
        "Equation of Motion for Rotational Systems": "The equation of motion for rotational systems is analogous to linear motion equations but uses angular displacement, velocity, and acceleration instead of linear quantities.",
        "Rotational Work": "Rotational work is the work done when a torque is applied to rotate an object, calculated as the product of torque and angular displacement.",
        "Precession": "Precession is the slow, circular movement of the axis of a rotating object, often observed in gyroscopes or spinning tops.",


    #Definition of Biology Topics
        "Genetics": "Genetics is the branch of biology that studies heredity and variation in organisms. It focuses on how traits are passed down from one generation to the next through genes.",
        "Gene": "A gene is a segment of DNA that contains the instructions for the synthesis of proteins, which ultimately determine an organism's traits. Genes are the basic unit of heredity.",
        "Chromosome": "A chromosome is a long DNA molecule that contains genetic information. Humans typically have 23 pairs of chromosomes, with each parent contributing one chromosome to each pair.",
        "Evolution": "Evolution is the process through which populations of organisms change over generations due to variations in traits and natural selection. It explains the diversity of life on Earth.",
        "Natural Selection": "Natural selection is the process by which organisms with traits better suited to their environment tend to survive and reproduce, passing those traits on to the next generation.",
        "Mutation": "A mutation is a change in the DNA sequence of an organism’s genome. Mutations can occur spontaneously or due to environmental factors, and can result in new traits or diseases.",
        "Homeostasis": "Homeostasis refers to the ability of an organism or system to maintain internal stability, despite changes in the external environment. This regulation is essential for survival.",
        "Mitosis": "Mitosis is a type of cell division that results in two genetically identical daughter cells. It is responsible for growth, repair, and asexual reproduction in multicellular organisms.",
        "Meiosis": "Meiosis is a type of cell division that reduces the chromosome number by half, producing four non-identical gametes. It is crucial for sexual reproduction and genetic diversity.",
        "Cell Membrane": "The cell membrane is a phospholipid bilayer that surrounds the cell, providing structure and regulating the movement of substances in and out of the cell.",
        "Nucleus": "The nucleus is the membrane-bound organelle in eukaryotic cells that contains the cell's genetic material (DNA). It controls cellular activities including growth, metabolism, and reproduction.",
        "Mitochondria": "Mitochondria are membrane-bound organelles in eukaryotic cells that generate energy in the form of ATP through cellular respiration. They are often called the powerhouse of the cell.",
        "Ribosome": "Ribosomes are cellular structures that synthesize proteins by translating messenger RNA (mRNA) into amino acid sequences. They can be found in the cytoplasm or attached to the endoplasmic reticulum.",
        "Endoplasmic Reticulum": "The endoplasmic reticulum (ER) is an organelle involved in the synthesis of proteins and lipids. The rough ER has ribosomes on its surface, while the smooth ER lacks ribosomes.",
        "Golgi Apparatus": "The Golgi apparatus is a cell organelle that processes and packages proteins and lipids. It modifies these molecules and directs them to their destination within or outside the cell.",
        "Lysosome": "Lysosomes are membrane-bound organelles containing enzymes that break down waste materials and cellular debris. They play a key role in cell digestion and waste removal.",
        "Cytoplasm": "The cytoplasm is the gel-like substance inside the cell membrane that surrounds the organelles. It is where most of the cell's metabolic processes occur.",
        "Vacuole": "A vacuole is a membrane-bound organelle in cells that stores water, nutrients, and waste products. In plant cells, vacuoles also help maintain cell turgor pressure.",
        "Photosynthesis": "Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy stored in glucose. This process requires sunlight, water, and carbon dioxide.",
        "Chloroplast": "Chloroplasts are organelles found in plant cells that contain the pigment chlorophyll. They are the site of photosynthesis, where light energy is converted into chemical energy.",
        "Biodiversity": "Biodiversity refers to the variety of life forms on Earth, including species diversity, genetic diversity, and ecosystem diversity. It is essential for ecosystem stability and resilience.",
        "Species": "A species is a group of organisms that can interbreed and produce fertile offspring under natural conditions. Species are the basic unit of classification in biology.",
        "Population": "A population is a group of individuals of the same species living in a specific area and interacting with each other. Populations can vary in size and density over time.",
        "Ecosystem": "An ecosystem is a biological community of interacting organisms and their physical environment. It includes both biotic (living) and abiotic (non-living) components that work together to maintain balance.",
        "Habitat": "A habitat is the natural environment in which an organism lives. It provides the necessary conditions for the organism's survival, including food, shelter, and mates for reproduction.",
        "Niche": "A niche is the role an organism plays in its ecosystem, including how it gets its food, interacts with other species, and contributes to the environment.",
        "Symbiosis": "Symbiosis is the interaction between two different organisms living in close physical proximity. It can be mutualistic (both benefit), commensal (one benefits, the other is unaffected), or parasitic (one benefits at the expense of the other).",
        "Predation": "Predation is an interaction in which one organism (the predator) kills and eats another organism (the prey). It plays a key role in regulating population sizes in ecosystems.",
        "Competition": "Competition occurs when two or more organisms vie for the same resource, such as food, water, or mates. It can occur within a species (intraspecific) or between different species (interspecific).",
        "Antibiotics": "Antibiotics are chemical substances that kill or inhibit the growth of bacteria. They are used to treat bacterial infections but are ineffective against viral infections.",
        "Virus": "A virus is a microscopic infectious agent that requires a host cell to replicate. It consists of genetic material (DNA or RNA) surrounded by a protein coat and can cause various diseases in organisms.",
        "Bacteria": "Bacteria are single-celled microorganisms that can exist in a variety of environments. They can be beneficial, such as those involved in nitrogen fixation, or harmful, causing diseases like tuberculosis.",
        "Fungi": "Fungi are a diverse group of eukaryotic organisms that include yeasts, molds, and mushrooms. They play essential roles in ecosystems as decomposers, breaking down organic material.",
        "Protist": "Protists are a diverse group of eukaryotic organisms that are mostly unicellular. They include algae, protozoa, and slime molds and can be found in various aquatic environments.",
        "Photosystem": "A photosystem is a protein complex in the chloroplast that absorbs light energy during photosynthesis. It converts light into chemical energy, which is used to synthesize sugars.",
        "Stomata": "Stomata are small pores found on the surface of leaves and stems. They allow for the exchange of gases, including the intake of carbon dioxide and the release of oxygen and water vapor.",
        "Fermentation": "Fermentation is a metabolic process that produces energy in the absence of oxygen. It is used by certain organisms, such as yeast, to convert sugars into alcohol and carbon dioxide.",
        "Biotechnology": "Biotechnology is the use of biological processes, organisms, or systems to develop new products or technologies. It includes applications in medicine, agriculture, and environmental science.",
        "Ecology": "Ecology is the study of the interactions between organisms and their environment. It includes the study of ecosystems, populations, and the impact of human activity on nature.",
        "Adaptation": "Adaptation is the process by which a species becomes better suited to its environment. It can involve structural, behavioral, or physiological changes that enhance survival and reproduction.",
        "Cell Theory": "Cell theory is the scientific theory that all living organisms are made up of cells, and that the cell is the basic unit of structure and function in organisms.",
        "Biomass": "Biomass refers to the total mass of living organisms in a given area or ecosystem at a particular time. It can also refer to organic material used as a renewable energy source.",
        "Asexual Reproduction": "Asexual reproduction is a mode of reproduction in which offspring are produced from a single parent. The offspring are genetically identical to the parent, as in binary fission in bacteria.",
        "Sexual Reproduction": "Sexual reproduction involves the fusion of two gametes, one from each parent, to form a new organism. It introduces genetic variation, which is essential for evolution.",
        "Enzyme": "An enzyme is a biological catalyst that accelerates chemical reactions in living organisms. Enzymes are highly specific and can be used to break down or build up various substrates.",
        "Zygote": "A zygote is the fertilized egg cell formed when a sperm cell fertilizes an egg cell. It contains the genetic material from both parents and will undergo cell division to form a new organism.",
        "Gene Expression": "Gene expression is the process by which information from a gene is used to produce a functional product, typically a protein. It involves transcription and translation processes.",
        "Biogenesis": "Biogenesis is the principle that living organisms arise only from pre-existing living organisms. It refutes the concept of spontaneous generation.",
        "Abiogenesis": "Abiogenesis is the theory that life can originate from non-living matter under certain conditions, which is considered a precursor to the study of biochemistry.",
        "Phospholipid Bilayer": "A phospholipid bilayer is the double layer of phospholipids that forms the structural basis of cell membranes, with hydrophobic tails and hydrophilic heads.",
        "Autotroph": "Autotrophs are organisms that produce their own food through photosynthesis or chemosynthesis, such as plants and certain bacteria.",
        "Heterotroph": "Heterotrophs are organisms that cannot produce their own food and must obtain energy by consuming other organisms, such as animals and fungi.",
        "Trophic Level": "A trophic level is a step in a food chain or web, representing an organism's position in the flow of energy. Producers occupy the first trophic level, followed by primary consumers, secondary consumers, etc.",
        "Prokaryote": "Prokaryotes are single-celled organisms that lack a membrane-bound nucleus and other organelles. Bacteria and archaea are examples of prokaryotes.",
        "Eukaryote": "Eukaryotes are organisms whose cells contain a nucleus and other organelles enclosed within membranes. Examples include plants, animals, and fungi.",
        "Flagellum": "A flagellum is a long, whip-like structure that protrudes from the cell body and is used for locomotion in some prokaryotic and eukaryotic cells.",
        "Cilia": "Cilia are short, hair-like structures that protrude from the surface of some cells and help with movement or the movement of substances around the cell.",
        "Endocytosis": "Endocytosis is the process by which cells engulf external substances by wrapping their membrane around them and bringing them inside the cell.",
        "Exocytosis": "Exocytosis is the process by which cells expel substances by fusing vesicles with the cell membrane, releasing the contents outside the cell.",
        "Cytoskeleton": "The cytoskeleton is a network of protein filaments and tubules that provides structural support, helps in cell division, and enables intracellular transport.",
        "Phagocytosis": "Phagocytosis is a type of endocytosis where a cell engulfs large particles such as dead cells or pathogens. It is often performed by white blood cells.",
        "Osmosis": "Osmosis is the movement of water molecules across a selectively permeable membrane from an area of lower solute concentration to an area of higher solute concentration.",
        "Diffusion": "Diffusion is the process by which molecules spread from an area of higher concentration to an area of lower concentration due to their random motion.",
        "Facilitated Diffusion": "Facilitated diffusion is a type of passive transport where specific molecules are transported across the cell membrane with the help of carrier proteins.",
        "Active Transport": "Active transport is the movement of molecules across the cell membrane against their concentration gradient, requiring energy in the form of ATP.",
        "ATP (Adenosine Triphosphate)": "ATP is the primary energy carrier in cells. It stores and transfers energy for various cellular processes, including metabolism and muscle contraction.",
        "RNA (Ribonucleic Acid)": "RNA is a single-stranded nucleic acid involved in protein synthesis and gene expression. It is synthesized from DNA and serves as a template for protein production.",
        "DNA (Deoxyribonucleic Acid)": "DNA is a double-stranded molecule that carries the genetic blueprint of an organism. It contains the instructions for building proteins and determines inheritance.",
        "Nucleotide": "A nucleotide is the basic building block of nucleic acids like DNA and RNA. It consists of a sugar, phosphate group, and nitrogenous base.",
        "Codon": "A codon is a sequence of three nucleotides in mRNA that specifies an amino acid or signals the end of protein synthesis.",
        "Anticodon": "An anticodon is a three-nucleotide sequence in tRNA that is complementary to a codon in mRNA, ensuring the correct amino acid is added during translation.",
        "Gene Pool": "The gene pool is the total collection of genetic material in a population of organisms, including all alleles for every gene in the population.",
        "Allele": "An allele is a variant form of a gene. Individuals inherit two alleles for each gene, one from each parent.",
        "Genotype": "The genotype is the genetic constitution of an organism, representing the combination of alleles inherited from both parents.",
        "Phenotype": "The phenotype is the observable physical or biochemical characteristics of an organism, which result from the interaction of its genotype with the environment.",
        "Homozygous": "An organism is homozygous for a gene if it has two identical alleles for that gene, one inherited from each parent.",
        "Heterozygous": "An organism is heterozygous for a gene if it has two different alleles for that gene, one inherited from each parent.",
        "Dominant Allele": "A dominant allele is an allele that expresses its trait even when only one copy is present, masking the effect of a recessive allele.",
        "Recessive Allele": "A recessive allele is an allele that only expresses its trait when two copies are present, with no dominant allele to mask it.",
        "Punnett Square": "A Punnett square is a diagram used to predict the outcome of a genetic cross. It shows the possible combinations of alleles in offspring.",
        "Mendel's Laws": "Mendel's laws of inheritance include the law of segregation (each parent contributes one allele for each gene) and the law of independent assortment (genes are inherited independently).",
        "Inbreeding": "Inbreeding is the breeding of closely related individuals, which increases the likelihood of recessive genetic disorders due to the increased chance of homozygous recessive alleles.",
        "Outbreeding": "Outbreeding is the mating of unrelated individuals, which promotes genetic diversity and reduces the risk of genetic disorders.",
        "Transcription": "Transcription is the process by which an RNA molecule is synthesized from a DNA template. It is the first step in gene expression.",
        "Translation": "Translation is the process by which a ribosome uses mRNA to synthesize a protein by linking amino acids in the correct order specified by the mRNA codons.",
        "RNA Splicing": "RNA splicing is the process by which non-coding regions (introns) are removed from the RNA transcript, and the remaining coding regions (exons) are joined together.",
        "Trophic Cascade": "A trophic cascade is an ecological phenomenon where the removal or addition of a top predator affects the abundance and distribution of lower trophic levels in an ecosystem.",
        "Food Chain": "A food chain is a linear sequence of organisms through which energy and nutrients flow. Each organism serves as food for the next in the chain.",
        "Food Web": "A food web is a complex network of interconnected food chains in an ecosystem. It shows how different organisms are related through feeding relationships.",
        "Keystone Species": "A keystone species is a species that has a disproportionately large effect on its ecosystem relative to its abundance or biomass. Its presence or absence significantly impacts the community structure.",
        "Carrying Capacity": "Carrying capacity is the maximum population size that an environment can support without degrading the ecosystem. It is determined by factors like food, shelter, and water availability.",
        "Ecological Succession": "Ecological succession is the process by which the structure of a biological community changes over time. It can be primary (starting from bare rock) or secondary (after a disturbance).",
        "Primary Producers": "Primary producers are organisms that produce their own food, such as plants and algae, using sunlight or chemicals. They form the base of an ecosystem's food chain.",
        "Primary Consumers": "Primary consumers are herbivores that feed on primary producers. They are the second trophic level in a food chain.",
        "Secondary Consumers": "Secondary consumers are carnivores or omnivores that eat primary consumers. They occupy the third trophic level in a food chain.",
        "Tertiary Consumers": "Tertiary consumers are apex predators that feed on secondary consumers. They occupy the top trophic level in a food chain.",
        "Decomposers": "Decomposers are organisms such as bacteria and fungi that break down dead organic material, recycling nutrients back into the ecosystem.",
        "Biogeochemical Cycles": "Biogeochemical cycles describe the movement of elements like carbon, nitrogen, and phosphorus through living organisms and the environment, maintaining ecosystem function.",
        "Carbon Cycle": "The carbon cycle is the process by which carbon is exchanged between the atmosphere, oceans, soil, and living organisms, maintaining carbon balance on Earth.",
        "Nitrogen Cycle": "The nitrogen cycle is the process by which nitrogen is converted between its various chemical forms, including nitrogen fixation, nitrification, denitrification, and ammonification.",
        "Phosphorus Cycle": "The phosphorus cycle describes the movement of phosphorus through the Earth's ecosystems. Unlike the carbon and nitrogen cycles, it does not involve a gaseous phase.",
        "Biomagnification": "Biomagnification is the increase in concentration of toxic substances, such as pesticides or heavy metals, in organisms at higher trophic levels within a food chain. As each level of the food chain consumes organisms from the level below, the toxins accumulate in their bodies, leading to higher concentrations of these substances in apex predators, such as large fish, birds of prey, or mammals, which can have harmful effects on their health and reproduction.",
        "Biome": "A biome is a large geographic biotic unit, a major community of plants and animals with similar life forms and environmental conditions, such as a desert or rainforest.",
        "Biodiversity": "Biodiversity refers to the variety of life forms in an ecosystem or on Earth, including the variety of species, genes, and ecosystems.",
        "Ecosystem": "An ecosystem is a community of living organisms interacting with each other and their physical environment, such as a forest, ocean, or pond.",
        "Adaptation": "Adaptation is a process by which organisms become better suited to their environment through natural selection, leading to changes in traits over generations.",
        "Natural Selection": "Natural selection is the process through which organisms with traits better suited to their environment are more likely to survive and reproduce, passing those traits to the next generation.",
        "Mutation": "A mutation is a change in the DNA sequence of an organism, which can lead to new traits and potentially affect survival or reproduction.",
        "Gene Expression": "Gene expression is the process by which information from a gene is used to synthesize a functional gene product, typically a protein.",
        "Reproductive Isolation": "Reproductive isolation occurs when two populations of the same species can no longer interbreed, leading to speciation over time.",
        "Speciation": "Speciation is the process by which one species splits into two or more distinct species due to genetic divergence and reproductive isolation.",
        "Cladistics": "Cladistics is a method of classifying organisms based on common ancestry and evolutionary relationships, using shared derived characteristics called synapomorphies.",
        "Phylogenetic Tree": "A phylogenetic tree is a diagram showing the evolutionary relationships among species, indicating how different species are related through common ancestors.",
        "Endangered Species": "Endangered species are species at risk of extinction due to habitat loss, overhunting, pollution, or other environmental factors.",
        "Extinction": "Extinction is the complete disappearance of a species from the Earth, often due to environmental changes, predation, or competition.",
        "Invasive Species": "Invasive species are non-native organisms that spread rapidly in a new environment and can cause harm to native species and ecosystems.",
        "Symbiosis": "Symbiosis is a close and long-term interaction between two different species, which can be mutualistic, commensalistic, or parasitic.",
        "Mutualism": "Mutualism is a type of symbiosis in which both organisms involved benefit from the relationship, such as bees and flowers.",
        "Commensalism": "Commensalism is a type of symbiosis where one organism benefits from the relationship, while the other is neither helped nor harmed, such as barnacles on a whale.",
        "Parasitism": "Parasitism is a type of symbiosis in which one organism benefits at the expense of the other, such as a tick feeding on a mammal.",
        "Conservation Biology": "Conservation biology is the scientific study of biodiversity and the efforts to protect and preserve species, habitats, and ecosystems.",
        "Endosymbiotic Theory": "The endosymbiotic theory suggests that certain organelles, such as mitochondria and chloroplasts, were once free-living bacteria that formed symbiotic relationships with early eukaryotic cells.",

    #Definition of Chemistry Topics
        "Acid": "An acid is a substance that donates protons (H+) when dissolved in water. Acids have a pH less than 7 and can turn blue litmus paper red.",
        "Base": "A base is a substance that accepts protons (H+) or donates hydroxide ions (OH-) in aqueous solutions. Bases have a pH greater than 7 and can turn red litmus paper blue.",
        "pH": "pH is a scale used to measure the acidity or basicity of a solution. It ranges from 0 to 14, with 7 being neutral, values less than 7 indicating acidic solutions, and values greater than 7 indicating basic solutions.",
        "Salt": "A salt is an ionic compound formed from the neutralization reaction between an acid and a base. Common salts include sodium chloride (NaCl).",
        "Ionic Bond": "An ionic bond is a type of chemical bond that occurs when one atom transfers electrons to another, resulting in the formation of positively and negatively charged ions that are attracted to each other.",
        "Covalent Bond": "A covalent bond is a type of chemical bond formed when two atoms share one or more pairs of electrons, typically occurring between nonmetal atoms.",
        "Mole": "A mole is a unit used to measure the amount of substance. One mole contains approximately 6.022 x 10^23 entities (atoms, molecules, or ions), known as Avogadro's number.",
        "Molarity": "Molarity is a measure of the concentration of a solute in a solution, expressed as moles of solute per liter of solution (mol/L).",
        "Stoichiometry": "Stoichiometry is the part of chemistry that deals with the calculation of reactants and products in chemical reactions, based on the conservation of mass and moles.",
        "Thermodynamics": "Thermodynamics is the branch of chemistry that deals with the relationships between heat, work, and energy. It includes the study of laws governing energy transformations and conversions.",
        "Entropy": "Entropy is a measure of the disorder or randomness in a system. In thermodynamics, it is a key concept in understanding the spontaneity of processes.",
        "Enthalpy": "Enthalpy is a thermodynamic quantity equivalent to the total heat content of a system. It is used to calculate the heat absorbed or released in a chemical reaction at constant pressure.",
        "Catalyst": "A catalyst is a substance that increases the rate of a chemical reaction by lowering the activation energy without being consumed in the reaction.",
        "Activation Energy": "Activation energy is the minimum amount of energy required to start a chemical reaction. It is necessary for breaking the bonds in reactant molecules.",
        "Redox Reaction": "A redox (reduction-oxidation) reaction involves the transfer of electrons between two substances. One substance loses electrons (oxidation), while another gains electrons (reduction).",
        "Isotope": "An isotope is a variant of a chemical element that has the same number of protons but a different number of neutrons, resulting in different atomic masses.",
        "Periodic Table": "The periodic table is a tabular arrangement of elements based on their atomic number, electron configurations, and recurring chemical properties.",
        "Atomic Number": "The atomic number of an element is the number of protons in its nucleus and determines the element's identity and its position in the periodic table.",
        "Atomic Mass": "The atomic mass of an element is the weighted average mass of the atoms of an element, taking into account the relative abundance of its isotopes.",
        "Electron": "An electron is a subatomic particle with a negative charge, found in the electron cloud surrounding the nucleus of an atom.",
        "Proton": "A proton is a subatomic particle with a positive charge, found in the nucleus of an atom. The number of protons in an atom determines its atomic number.",
        "Neutron": "A neutron is a subatomic particle with no charge, found in the nucleus of an atom. Neutrons, along with protons, contribute to an atom's mass.",
        "Valence Electrons": "Valence electrons are the electrons in the outermost shell of an atom. They are involved in chemical bonding and determine an atom's reactivity.",
        "Periodic Law": "The periodic law states that the properties of elements are periodic functions of their atomic numbers, meaning elements with similar properties occur at regular intervals when arranged by atomic number.",
        "Molecular Formula": "The molecular formula of a compound shows the number and types of atoms in a molecule, represented by chemical symbols and subscripts (e.g., H2O for water).",
        "Empirical Formula": "The empirical formula is the simplest whole-number ratio of the elements in a compound, representing the proportions of the elements, but not the exact number of atoms.",
        "Empirical Rule": "The empirical rule (also known as the octet rule) states that atoms tend to gain, lose, or share electrons to achieve a full outer electron shell, typically consisting of eight electrons.",
        "Solubility": "Solubility is the ability of a substance to dissolve in a solvent to form a homogeneous solution. It depends on factors like temperature, pressure, and the nature of the solute and solvent.",
        "Solvent": "A solvent is a substance that dissolves a solute to form a solution. Water is often referred to as the universal solvent due to its ability to dissolve many substances.",
        "Solute": "A solute is a substance that is dissolved in a solvent to form a solution. Common examples include sugar or salt dissolved in water.",
        "Vaporization": "Vaporization is the process by which a liquid changes into a gas, either through evaporation or boiling. It occurs when the liquid molecules gain enough energy to overcome intermolecular forces.",
        "Condensation": "Condensation is the process by which a gas turns into a liquid when cooled. It occurs when gas molecules lose enough energy to form intermolecular bonds.",
        "Sublimation": "Sublimation is the phase transition in which a solid changes directly into a gas without passing through the liquid phase. An example is the sublimation of dry ice (solid CO2).",
        "Deposition": "Deposition is the process by which a gas turns directly into a solid without first becoming a liquid. It is the reverse of sublimation, such as the formation of frost from water vapor.",
        "Gas Laws": "Gas laws describe the behavior of gases under different conditions of temperature, pressure, and volume. The main gas laws include Boyle's law, Charles's law, and Avogadro's law.",
        "Boyle's Law": "Boyle's Law states that the pressure of a given amount of gas is inversely proportional to its volume at constant temperature. Mathematically, P ∝ 1/V.",
        "Charles's Law": "Charles's Law states that the volume of a gas is directly proportional to its temperature at constant pressure. Mathematically, V ∝ T.",
        "Avogadro's Law": "Avogadro's Law states that equal volumes of gases, at the same temperature and pressure, contain an equal number of molecules. This law relates volume to the number of molecules in a gas.",
        "Ideal Gas Law": "The ideal gas law is an equation of state for a gas, combining Boyle's, Charles's, and Avogadro's laws. It is expressed as PV = nRT, where P is pressure, V is volume, n is moles, R is the ideal gas constant, and T is temperature.",
        "Kinetic Molecular Theory": "The kinetic molecular theory explains the behavior of gases. It states that gas molecules are in constant random motion, and the collisions between them are elastic and result in pressure.",
        "Heat Capacity": "Heat capacity is the amount of heat energy required to raise the temperature of a substance by one degree Celsius. It depends on the substance's mass and specific heat.",
        "Specific Heat": "Specific heat is the amount of heat required to raise the temperature of one gram of a substance by one degree Celsius. Different substances have different specific heats.",
        "Latent Heat": "Latent heat is the heat energy required to change the phase of a substance without changing its temperature. Examples include the latent heat of fusion (solid to liquid) and latent heat of vaporization (liquid to gas).",
        "Acid-Base Titration": "An acid-base titration is a laboratory method used to determine the concentration of an acid or base in a solution by neutralizing it with a solution of known concentration.",
        "Molar Mass": "Molar mass is the mass of one mole of a substance, expressed in grams per mole (g/mol). It is numerically equal to the atomic or molecular mass in atomic mass units (amu).",
        "Electrochemistry": "Electrochemistry is the study of the relationship between electricity and chemical reactions. It involves the study of processes such as oxidation, reduction, and the functioning of batteries.",
        "Electrolyte": "An electrolyte is a substance that conducts electricity when dissolved in water, due to the presence of ions. Examples include sodium chloride and potassium nitrate.",
        "Oxidation": "Oxidation is the loss of electrons from a substance, often accompanied by an increase in oxidation state. It occurs in redox reactions, where the substance that loses electrons is oxidized.",
        "Reduction": "Reduction is the gain of electrons by a substance, often accompanied by a decrease in oxidation state. It occurs in redox reactions, where the substance that gains electrons is reduced.",
        "Oxidizing Agent": "An oxidizing agent is a substance that causes another substance to undergo oxidation by accepting electrons. It is itself reduced in the process.",
        "Reducing Agent": "A reducing agent is a substance that causes another substance to undergo reduction by donating electrons. It is itself oxidized in the process.",
        "Alkali": "An alkali is a water-soluble base that releases hydroxide ions (OH-) in solution. Alkalis include substances such as sodium hydroxide (NaOH) and potassium hydroxide (KOH).",
        "Alkaline Earth Metals": "Alkaline earth metals are a group of elements found in Group 2 of the periodic table. They include beryllium, magnesium, calcium, strontium, barium, and radium.",
        "Transition Metals": "Transition metals are elements found in the central block of the periodic table (Groups 3 to 12). They are characterized by their ability to form multiple oxidation states and their use as catalysts.",
        "Halogens": "Halogens are elements found in Group 17 of the periodic table. They include fluorine, chlorine, bromine, iodine, and astatine, and are known for their high reactivity and ability to form salts with metals.",
        "Noble Gases": "Noble gases are the elements found in Group 18 of the periodic table. These gases, including helium, neon, argon, krypton, xenon, and radon, are chemically inert due to their full electron shells.",
        "Periodic Trend": "Periodic trends refer to the patterns observed in the properties of elements as you move across or down the periodic table. Examples include trends in atomic size, electronegativity, and ionization energy.",
        "Ionization Energy": "Ionization energy is the amount of energy required to remove an electron from an atom or ion in the gas phase. It generally increases across a period and decreases down a group.",
        "Electronegativity": "Electronegativity is the measure of an atom's ability to attract and bond with electrons. Elements with high electronegativity, such as fluorine, tend to attract electrons more strongly.",
        "Atomic Radius": "Atomic radius is the distance from the nucleus to the outermost electron shell of an atom. It generally decreases across a period and increases down a group.",
        "Chemical Bond": "A chemical bond is the force that holds two atoms together in a molecule. There are three primary types: ionic bonds, covalent bonds, and metallic bonds.",
        "Polyatomic Ion": "A polyatomic ion is an ion composed of two or more atoms covalently bonded that act as a single unit with an overall charge. Examples include sulfate (SO4^2-) and ammonium (NH4+).",
        "Hydrogen Bond": "A hydrogen bond is a weak bond formed when a hydrogen atom attached to an electronegative atom, such as oxygen or nitrogen, is attracted to another electronegative atom.",
        "Van der Waals Forces": "Van der Waals forces are weak intermolecular forces that include dipole-dipole interactions, London dispersion forces, and hydrogen bonding. They are important in the behavior of gases and liquids.",
        "Le Chatelier's Principle": "Le Chatelier's principle states that if a dynamic equilibrium is disturbed by changing the conditions (e.g., concentration, temperature, or pressure), the system will adjust to counteract the change.",
        "Solubility Product": "The solubility product is an equilibrium constant that expresses the solubility of a salt in water. It is used to calculate the concentrations of ions in a saturated solution.",
        "Buffer Solution": "A buffer solution is a solution that resists changes in pH when small amounts of an acid or base are added. It is typically composed of a weak acid and its conjugate base or a weak base and its conjugate acid.",
        "Acidic Solution": "An acidic solution has a pH value less than 7 and contains a higher concentration of hydrogen ions (H+) than hydroxide ions (OH-).",
        "Basic Solution": "A basic solution has a pH value greater than 7 and contains a higher concentration of hydroxide ions (OH-) than hydrogen ions (H+).",
        "Titration": "Titration is a laboratory technique used to determine the concentration of a solution by adding a titrant of known concentration to a solution of unknown concentration until the reaction reaches the equivalence point.",
        "Molecular Geometry": "Molecular geometry is the three-dimensional arrangement of atoms in a molecule. It is determined by the number of bonding and lone pairs of electrons around a central atom.",
        "Valence Shell Electron Pair Repulsion (VSEPR) Theory": "VSEPR theory predicts the shape of a molecule based on the repulsion between electron pairs in the valence shell of atoms, aiming to minimize electron pair repulsion.",
        "Resonance": "Resonance occurs when a molecule can be represented by two or more valid Lewis structures. The actual structure is a hybrid of these resonance forms.",
        "Aromaticity": "Aromaticity refers to the stability and special characteristics of molecules containing conjugated ring systems that follow Huckel's rule, such as benzene.",
        "Saturated Hydrocarbon": "A saturated hydrocarbon is a hydrocarbon compound that contains only single bonds between carbon atoms. Examples include alkanes like methane and ethane.",
        "Unsaturated Hydrocarbon": "An unsaturated hydrocarbon is a hydrocarbon that contains one or more double or triple bonds between carbon atoms. Examples include alkenes and alkynes.",
        "Functional Group": "A functional group is a specific group of atoms within a molecule that is responsible for the chemical properties of the compound. Examples include hydroxyl (-OH), carboxyl (-COOH), and amine (-NH2).",
        "Isomer": "Isomers are compounds that have the same molecular formula but differ in the arrangement of atoms or the spatial orientation of their atoms. There are structural isomers and stereoisomers.",
        "Electrophile": "An electrophile is a molecule or ion that accepts an electron pair from a nucleophile in a chemical reaction. Electrophiles are typically electron-deficient species.",
        "Nucleophile": "A nucleophile is a molecule or ion that donates an electron pair to form a new chemical bond with an electrophile. Nucleophiles are typically electron-rich species.",
        "Sn1 Reaction": "An SN1 reaction (Substitution Nucleophilic Unimolecular) is a type of substitution reaction in which the rate-determining step involves the departure of a leaving group, forming a carbocation intermediate.",
        "Sn2 Reaction": "An SN2 reaction (Substitution Nucleophilic Bimolecular) is a type of substitution reaction in which the nucleophile attacks the electrophile and the leaving group departs simultaneously, in a one-step mechanism.",
        "E1 Reaction": "An E1 reaction (Elimination Unimolecular) is a type of elimination reaction where the rate-determining step involves the departure of a leaving group, forming a carbocation intermediate that undergoes elimination.",
        "E2 Reaction": "An E2 reaction (Elimination Bimolecular) is a type of elimination reaction where a base abstracts a proton from a carbon adjacent to the leaving group, leading to the simultaneous departure of the leaving group and the formation of a double bond.",
        "Aldehyde": "An aldehyde is a type of organic compound characterized by a carbonyl group (C=O) bonded to at least one hydrogen atom. A common example is formaldehyde.",
        "Ketone": "A ketone is an organic compound containing a carbonyl group (C=O) bonded to two carbon atoms. Acetone is a common example of a ketone.",
        "Carboxylic Acid": "A carboxylic acid is an organic compound that contains a carboxyl group (-COOH), which consists of a carbonyl group (C=O) and a hydroxyl group (-OH). Acetic acid is a well-known example.",
        "Ester": "An ester is an organic compound derived from a carboxylic acid and an alcohol. It has the general formula RCOOR' and is often responsible for pleasant smells in fruits and flowers.",
        "Amine": "An amine is an organic compound derived from ammonia (NH3) by replacing one or more hydrogen atoms with alkyl or aryl groups. Amines are commonly found in biological molecules like amino acids.",
        "Amide": "An amide is an organic compound that contains a carbonyl group (C=O) bonded to a nitrogen atom. Amides are important in biological processes and are the building blocks of proteins.",
        "Polymer": "A polymer is a large molecule composed of repeating structural units, known as monomers. Examples of polymers include plastic materials like polyethylene and biological molecules like DNA.",
        "Nucleic Acid": "Nucleic acids are biological molecules that carry genetic information. DNA (deoxyribonucleic acid) and RNA (ribonucleic acid) are the primary nucleic acids found in living organisms.",
        "Enzyme": "An enzyme is a biological catalyst that speeds up the rate of a chemical reaction without being consumed in the process. Enzymes are essential for metabolic processes in living organisms.",
        "Ligand": "A ligand is an ion or molecule that binds to a central metal atom or ion to form a coordination complex. Ligands can be anions or neutral molecules, such as water or ammonia.",
        "Coordination Complex": "A coordination complex is a molecule or ion formed by a central metal atom or ion bonded to surrounding ligands. These complexes often play key roles in chemical reactions and catalysis.",
        "Catalyst": "A catalyst is a substance that increases the rate of a chemical reaction without being consumed in the reaction. Catalysts work by lowering the activation energy of the reaction.",
        "Heterogeneous Catalyst": "A heterogeneous catalyst is a catalyst that exists in a different phase than the reactants. For example, solid catalysts are often used in reactions involving gaseous reactants.",
        "Homogeneous Catalyst": "A homogeneous catalyst is a catalyst that exists in the same phase as the reactants, typically in solutions. An example is the use of acid or base in certain organic reactions.",
        "Activation Energy": "Activation energy is the minimum energy required for a chemical reaction to occur. It represents the energy barrier that must be overcome for reactants to be converted to products.",
        "Equilibrium Constant (K)": "The equilibrium constant (K) is a numerical value that expresses the ratio of the concentrations of products to reactants at equilibrium, for a given reaction at a specific temperature.",
        "Dynamic Equilibrium": "Dynamic equilibrium is a state in which the concentrations of reactants and products remain constant over time, although both the forward and reverse reactions continue to occur.",
        "Acid-Base Titration": "Acid-base titration is a method used to determine the concentration of an unknown acid or base by reacting it with a known volume and concentration of a titrant.",
        "Molarity (M)": "Molarity is the concentration of a solution, expressed as the number of moles of solute per liter of solution. It is commonly used to prepare solutions in laboratory experiments.",
        "Molality (m)": "Molality is the concentration of a solution, expressed as the number of moles of solute per kilogram of solvent. Unlike molarity, molality is independent of temperature.",
        "Normality (N)": "Normality is a measure of concentration equal to the equivalent number of reactive units per liter of solution. It is used in acid-base and redox reactions.",
        "Colligative Properties": "Colligative properties are properties of solutions that depend on the number of solute particles in a given quantity of solvent, such as boiling point elevation and freezing point depression.",
        "Boiling Point Elevation": "Boiling point elevation is the increase in the boiling point of a solvent when a non-volatile solute is added, as a result of the reduction in vapor pressure of the solvent.",
        "Freezing Point Depression": "Freezing point depression is the decrease in the freezing point of a solvent when a solute is added, due to the disruption of the solvent's ability to form a solid.",
        "Raoult's Law": "Raoult's law states that the vapor pressure of a solvent in a solution is directly proportional to the mole fraction of the solvent. It is used to explain colligative properties.",
        "Ideal Gas": "An ideal gas is a hypothetical gas that follows the ideal gas law perfectly, with no interactions between gas molecules and the molecules having negligible volume.",
        "Real Gas": "A real gas is a gas that deviates from ideal behavior due to intermolecular forces and the finite volume of gas molecules, especially at high pressures and low temperatures.",
        "Boyle's Law": "Boyle's law states that the pressure of a given amount of gas is inversely proportional to its volume at constant temperature, i.e., PV = constant.",
        "Charles's Law": "Charles's law states that the volume of a given amount of gas is directly proportional to its absolute temperature at constant pressure, i.e., V/T = constant.",
        "Avogadro's Law": "Avogadro's law states that equal volumes of gases at the same temperature and pressure contain an equal number of molecules, i.e., V/n = constant.",
        "Ideal Gas Law": "The ideal gas law combines Boyle's, Charles's, and Avogadro's laws into one equation: PV = nRT, where P is pressure, V is volume, n is the number of moles, R is the gas constant, and T is temperature.",
        "Dalton's Law of Partial Pressures": "Dalton's law states that the total pressure exerted by a mixture of non-reacting gases is equal to the sum of the partial pressures of each gas in the mixture.",
        "Graham's Law of Diffusion": "Graham's law of diffusion states that the rate of diffusion of a gas is inversely proportional to the square root of its molar mass, i.e., rate ∝ 1/√M.",
        "Electrochemical Cell": "An electrochemical cell is a device that generates electrical energy from chemical reactions, such as in a battery or fuel cell. It consists of two electrodes and an electrolyte.",
        "Galvanic Cell": "A galvanic cell is a type of electrochemical cell that generates electrical energy from spontaneous redox reactions. The most common example is a battery.",
        "Electrolysis": "Electrolysis is the process of using an electric current to drive a non-spontaneous chemical reaction. It is used in the extraction of metals and electroplating.",
        "Faraday's Laws of Electrolysis": "Faraday's laws of electrolysis relate the amount of substance altered at an electrode to the quantity of electric charge passed through the electrolyte during electrolysis.",
        "Standard Electrode Potential": "Standard electrode potential is the measure of the tendency of a half-reaction to occur as a reduction, measured under standard conditions. It is used to calculate the overall cell potential.",
        "Cell Potential": "Cell potential (or electromotive force, emf) is the potential difference between the two electrodes of an electrochemical cell. It determines the driving force for electron flow.",
        "Redox Reaction": "A redox reaction is a chemical reaction in which one substance is oxidized (loses electrons) and another is reduced (gains electrons).",
        "Oxidation Number": "Oxidation number (or oxidation state) is a number assigned to an element in a compound that represents the number of electrons it has gained or lost relative to its elemental state.",
        "Endothermic Reaction": "An endothermic reaction is a chemical reaction that absorbs heat from its surroundings, leading to a decrease in the temperature of the system.",
        "Exothermic Reaction": "An exothermic reaction is a chemical reaction that releases heat to its surroundings, leading to an increase in the temperature of the system.",
        "Heat of Formation": "The heat of formation is the change in enthalpy when one mole of a compound is formed from its elements in their standard states.",
        "Hess's Law": "Hess's law states that the total enthalpy change of a reaction is the sum of the enthalpy changes of the individual steps of the reaction, regardless of the pathway taken.",
        "Entropy (S)": "Entropy is a measure of the disorder or randomness in a system. It tends to increase in spontaneous processes and is a key factor in determining the spontaneity of reactions.",
        "Gibbs Free Energy": "Gibbs free energy is a thermodynamic quantity that combines enthalpy, temperature, and entropy to predict the spontaneity of a process. If ΔG is negative, the process is spontaneous.",
        "Thermodynamic Equilibrium": "Thermodynamic equilibrium is the state in which the macroscopic properties of a system, such as pressure, temperature, and composition, are constant over time.",
        "Concentration Cell": "A concentration cell is a type of electrochemical cell in which the two half-cells have the same electrode but different concentrations of ions.",
        "Saturated Solution": "A saturated solution is a solution that contains the maximum amount of solute that can dissolve at a given temperature and pressure. Any excess solute will not dissolve.",
        "Supersaturated Solution": "A supersaturated solution is a solution that contains more solute than is normally possible at a given temperature. It is unstable and can precipitate the excess solute.",
        "Precipitate": "A precipitate is a solid that forms and separates from a solution during a chemical reaction, typically when the solution becomes saturated with a product.",
        "Polarity": "Polarity refers to the distribution of electrical charge over the atoms in a molecule. Polar molecules have an uneven distribution of charge, leading to positive and negative regions.",
        "London Dispersion Forces": "London dispersion forces are weak intermolecular forces caused by the temporary fluctuations in electron density that induce dipoles in neighboring molecules.",
        "Dipole-Dipole Interactions": "Dipole-dipole interactions are intermolecular forces that occur between polar molecules, where the positive end of one molecule is attracted to the negative end of another.",
        "Covalent Bond": "A covalent bond is a chemical bond formed when two atoms share one or more pairs of electrons. Covalent bonds occur between nonmetals and can be single, double, or triple.",
        "Ionic Bond": "An ionic bond is a chemical bond formed when one atom donates electrons to another, creating positively and negatively charged ions that are held together by electrostatic forces.",
        "Metallic Bond": "A metallic bond is a type of bond in which electrons are free to move through a lattice of metal cations. This bond accounts for properties such as electrical conductivity and malleability in metals.",


    #Definition of Mathematics Topics
        "Abelian Group": "An abelian group is a group in which the group operation is commutative, meaning that the order of operations does not affect the result (a * b = b * a for all elements a and b).",
        "Absolute Value": "The absolute value of a number is its distance from zero on the number line, regardless of direction. It is denoted as |x| and is always non-negative.",
        "Acute Angle": "An acute angle is an angle that measures less than 90 degrees.",
        "Algorithm": "An algorithm is a step-by-step procedure or formula for solving a problem or performing a task.",
        "Alternate Interior Angles": "Alternate interior angles are two angles on opposite sides of a transversal but inside the two lines it intersects. These angles are congruent if the lines are parallel.",
        "Angle": "An angle is formed by two rays that share a common endpoint, called the vertex.",
        "Area": "The area of a shape is the measure of the surface enclosed by the shape, typically measured in square units.",
        "Associative Property": "The associative property states that the grouping of numbers in an operation does not affect the result, i.e., (a + b) + c = a + (b + c) for addition.",
        "Axis": "An axis is a reference line used in geometry or graphing to measure distances and angles. The most common axes are the x-axis and y-axis in a two-dimensional coordinate system.",
        "Base": "In a logarithm, the base is the number that is raised to a power to obtain a given value. For example, in log₁₀(100), the base is 10.",
        "Binomial Theorem": "The binomial theorem provides a formula for expanding expressions that are raised to a power, such as (a + b)^n.",
        "Calculator": "A calculator is a device or software used to perform mathematical calculations.",
        "Chord": "A chord is a line segment connecting two points on a curve, such as the ends of a diameter in a circle.",
        "Circle": "A circle is a set of all points in a plane that are at a fixed distance (radius) from a given point (the center).",
        "Class": "In set theory, a class is a collection of sets or objects, often defined by a property or condition that the objects satisfy.",
        "Commutative Property": "The commutative property states that the order of operations does not affect the result, i.e., a + b = b + a or a * b = b * a.",
        "Complex Number": "A complex number is a number in the form a + bi, where a and b are real numbers, and i is the imaginary unit (√-1).",
        "Compound Interest": "Compound interest is the interest calculated on both the initial principal and the accumulated interest from previous periods.",
        "Congruence": "Two objects or figures are congruent if they have the same shape and size, meaning one can be transformed into the other by translation, rotation, or reflection.",
        "Cone": "A cone is a three-dimensional geometric figure with a circular base and a single vertex not in the plane of the base.",
        "Congruent Angles": "Two angles are congruent if they have the same measure.",
        "Continuity": "A function is continuous if small changes in the input result in small changes in the output, with no jumps or breaks in the graph of the function.",
        "Coordinate": "A coordinate is a set of values that define a point's position in a particular space, such as (x, y) in two dimensions.",
        "Cosine": "Cosine is a trigonometric function that relates the angle of a right triangle to the ratio of the adjacent side to the hypotenuse.",
        "Cubic Function": "A cubic function is a polynomial function of degree three, generally in the form f(x) = ax³ + bx² + cx + d.",
        "Cube Root": "The cube root of a number is the value that, when multiplied by itself three times, gives the original number. It is denoted as ∛x.",
        "Derivative": "The derivative of a function measures how the function's output changes as its input changes, i.e., the slope of the tangent line to the graph at a given point.",
        "Determinant": "The determinant is a scalar value that can be computed from the elements of a square matrix and provides important information about the matrix, such as invertibility.",
        "Diagonal": "A diagonal is a line segment connecting two non-adjacent vertices in a polygon or polyhedron.",
        "Digit": "A digit is a single number from 0 to 9, used to represent numerical values.",
        "Difference": "The difference is the result of subtracting one number from another.",
        "Divisor": "A divisor is a number that divides another number exactly, without leaving a remainder.",
        "Dividend": "The dividend is the number being divided in a division operation.",
        "Distributive Property": "The distributive property states that for any numbers a, b, and c, a(b + c) = ab + ac.",
        "Ellipse": "An ellipse is a curve in a plane defined as the set of points where the sum of the distances from two fixed points (foci) is constant.",
        "Exponent": "An exponent is a number that indicates how many times a base is multiplied by itself, as in a^n.",
        "Factor": "A factor is a number or algebraic expression that divides another number or expression exactly, without leaving a remainder.",
        "Factorial": "The factorial of a number n (denoted n!) is the product of all positive integers from 1 to n.",
        "Fibonacci Sequence": "The Fibonacci sequence is a series of numbers in which each number is the sum of the two preceding ones, typically starting with 0 and 1.",
        "Finite Set": "A finite set is a set that contains a specific, countable number of elements.",
        "First Derivative Test": "The first derivative test is a method used to determine the local maxima and minima of a function by analyzing the sign of its derivative.",
        "Fraction": "A fraction represents a part of a whole and is written as a/b, where a is the numerator and b is the denominator.",
        "Frequency": "Frequency is the number of occurrences of a repeating event within a given period.",
        "Function": "A function is a relation between a set of inputs and a set of possible outputs, where each input is related to exactly one output.",
        "Geometric Mean": "The geometric mean of a set of n numbers is the nth root of the product of the numbers.",
        "Graph": "A graph is a visual representation of data or mathematical relationships, often consisting of vertices (nodes) connected by edges (lines).",
        "Greatest Common Divisor (GCD)": "The greatest common divisor of two numbers is the largest number that divides both of them exactly.",
        "Group": "In abstract algebra, a group is a set of elements equipped with an operation that satisfies four properties: closure, associativity, identity, and invertibility.",
        "Half-Life": "The half-life of a substance is the time required for half of the substance to decay or transform into another substance.",
        "Height": "The height of a figure is the perpendicular distance from the base to the top or apex.",
        "Histogram": "A histogram is a graphical representation of the distribution of a set of data, using bars to represent the frequency of data in intervals.",
        "Hypotenuse": "The hypotenuse is the longest side of a right triangle, opposite the right angle.",
        "Identity Element": "The identity element is an element in a group that, when combined with any element in the group, leaves that element unchanged.",
        "Imaginary Number": "An imaginary number is a number that can be written as a real number multiplied by the imaginary unit i, where i = √-1.",
        "Inequality": "An inequality is a mathematical relationship that compares two expressions, such as a < b, a > b, or a ≤ b.",
        "Integer": "An integer is any whole number, positive, negative, or zero, that does not include fractions or decimals.",
        "Intersection": "The intersection of two sets is the set of elements that are common to both sets.",
        "Interval": "An interval is a range of numbers between two endpoints, either including or excluding the endpoints.",
        "Inverse": "The inverse of a number or operation is the opposite or reverse of the original, such as the multiplicative inverse 1/x.",
        "Irrational Number": "An irrational number is a number that cannot be expressed as a fraction of two integers, and its decimal expansion is non-repeating and non-terminating.",
        "Isosceles Triangle": "An isosceles triangle is a triangle that has two sides of equal length.",
        "Lateral Surface Area": "The lateral surface area of a three-dimensional object is the total area of its sides, excluding the base and top.",
        "Least Common Denominator (LCD)": "The least common denominator is the smallest common multiple of the denominators of two or more fractions.",
        "Least Common Multiple (LCM)": "The least common multiple of two or more numbers is the smallest positive number that is divisible by all the numbers.",
        "Leg": "A leg is one of the sides of a right triangle, specifically the sides that are adjacent to the right angle.",
        "Linear Equation": "A linear equation is an equation in which the highest power of the variable is one. It represents a straight line when graphed on a coordinate plane.",
        "Logarithm": "A logarithm is the inverse operation to exponentiation, answering the question: to what power must a base be raised to produce a given number?",
        "Matrix": "A matrix is a rectangular array of numbers arranged in rows and columns, used to represent linear transformations or systems of linear equations.",
        "Mean": "The mean is the sum of a set of values divided by the number of values in the set. It is commonly known as the average.",
        "Median": "The median is the middle value in a data set when the values are arranged in ascending or descending order. If there is an even number of values, the median is the average of the two middle values.",
        "Mode": "The mode is the value that appears most frequently in a data set.",
        "Monomial": "A monomial is an algebraic expression consisting of one term, which may be a constant, a variable, or a product of constants and variables.",
        "Multiplicative Identity": "The multiplicative identity is the number 1, because multiplying any number by 1 leaves the number unchanged.",
        "Multiplicative Inverse": "The multiplicative inverse of a number is another number that, when multiplied by the original number, gives the result of 1.",
        "Natural Numbers": "Natural numbers are the set of positive integers starting from 1, used for counting and ordering.",
        "Negative Numbers": "Negative numbers are numbers that are less than zero and represent values on the left side of the number line.",
        "Nonagon": "A nonagon is a polygon with nine sides and nine angles.",
        "Number Line": "A number line is a straight line on which numbers are marked at intervals, used to represent numbers in a visual manner.",
        "Numerator": "The numerator is the top part of a fraction, indicating how many parts of the whole are being considered.",
        "Octagon": "An octagon is a polygon with eight sides and eight angles.",
        "Operation": "An operation is a mathematical procedure, such as addition, subtraction, multiplication, or division, applied to numbers or expressions.",
        "Obtuse Angle": "An obtuse angle is an angle that measures more than 90 degrees but less than 180 degrees.",
        "Open Interval": "An open interval is an interval in which the endpoints are not included, denoted as (a, b).",
        "Opposite Numbers": "Opposite numbers are two numbers that are equidistant from zero on the number line but have opposite signs.",
        "Ordered Pair": "An ordered pair is a pair of numbers written in a specific order, typically in the form (x, y), used to represent points on the coordinate plane.",
        "Origin": "The origin is the point of intersection of the x-axis and y-axis in a two-dimensional coordinate system, typically represented as (0, 0).",
        "Parallel Lines": "Parallel lines are two lines in a plane that never meet, no matter how far they are extended.",
        "Parabola": "A parabola is a U-shaped curve that is the graph of a quadratic function, y = ax² + bx + c.",
        "Percent": "A percent is a ratio expressed as a fraction of 100, represented by the symbol %. It is often used to express how much one quantity is of another.",
        "Perimeter": "The perimeter of a shape is the total length of its boundary or sides.",
        "Permutation": "A permutation is an arrangement of objects or elements in a specific order. The number of permutations of a set of objects is calculated as n!, where n is the number of objects.",
        "Pi": "Pi (π) is a mathematical constant representing the ratio of a circle's circumference to its diameter, approximately equal to 3.14159.",
        "Plane": "A plane is a flat, two-dimensional surface that extends infinitely in all directions.",
        "Pythagorean Theorem": "The Pythagorean theorem states that in a right-angled triangle, the square of the length of the hypotenuse is equal to the sum of the squares of the lengths of the other two sides. It is expressed as a² + b² = c².",
        "Quadrant": "A quadrant is one of the four regions into which the coordinate plane is divided by the x-axis and y-axis.",
        "Quadratic Equation": "A quadratic equation is a second-degree polynomial equation, typically in the form ax² + bx + c = 0, where a, b, and c are constants.",
        "Radical": "A radical is an expression that involves roots, such as square roots or cube roots.",
        "Rational Number": "A rational number is any number that can be expressed as the quotient of two integers, where the denominator is not zero.",
        "Ray": "A ray is a part of a line that starts at a point and extends infinitely in one direction.",
        "Rectangle": "A rectangle is a four-sided polygon with opposite sides equal in length and four right angles.",
        "Reflection": "A reflection is a transformation that flips a figure over a line, creating a mirror image.",
        "Rhombus": "A rhombus is a quadrilateral with all four sides of equal length, but not necessarily with right angles.",
        "Right Angle": "A right angle is an angle that measures exactly 90 degrees.",
        "Right Triangle": "A right triangle is a triangle with one angle measuring 90 degrees.",
        "Roots": "Roots are values of a variable that satisfy an equation, making the equation true.",
        "Scalene Triangle": "A scalene triangle is a triangle in which all three sides have different lengths and all three angles have different measures.",
        "Scientific Notation": "Scientific notation is a way of expressing very large or very small numbers as a product of a number between 1 and 10 and a power of 10.",
        "Sequence": "A sequence is an ordered list of numbers or terms, where each term follows a specific pattern or rule.",
        "Series": "A series is the sum of the terms in a sequence.",
        "Slope": "The slope of a line is a measure of how steep the line is. It is calculated as the change in y divided by the change in x (rise over run).",
        "Sphere": "A sphere is a three-dimensional object where all points on the surface are equidistant from the center.",
        "Square": "A square is a quadrilateral with four equal sides and four right angles.",
        "Square Root": "The square root of a number is a value that, when multiplied by itself, gives the original number. It is denoted as √x.",
        "Subtraction": "Subtraction is the mathematical operation of taking one number away from another.",
        "Supplementary Angles": "Supplementary angles are two angles whose measures add up to 180 degrees.",
        "Symmetry": "Symmetry is a property of a figure that allows it to be divided into parts that are identical or mirror images of each other.",
        "Tangent": "The tangent of an angle in a right triangle is the ratio of the opposite side to the adjacent side.",
        "Term": "A term is a single number, variable, or the product of numbers and variables in an expression.",
        "Theorem": "A theorem is a statement that has been proven based on previously established facts or axioms.",
        "Triangle": "A triangle is a polygon with three sides and three angles.",
        "Trinomial": "A trinomial is a polynomial consisting of three terms.",
        "Union": "The union of two sets is the set of all elements that are in either of the sets.",
        "Unique Solution": "A unique solution is a solution to an equation or system of equations that is the only solution.",
        "Universal Set": "The universal set is the set that contains all possible elements for a particular context or problem.",
        "Variable": "A variable is a symbol, often a letter, that represents an unknown or changeable value in mathematical expressions or equations.",
        "Venn Diagram": "A Venn diagram is a visual representation of sets and their relationships, typically using circles to represent different sets.",
        "Vertex": "A vertex is a point where two or more lines or edges meet, such as the corner of a polygon or polyhedron.",
        "Volume": "Volume is the amount of space occupied by a three-dimensional object, measured in cubic units.",
        "X-Axis": "The x-axis is the horizontal axis in a two-dimensional coordinate system, typically used to represent the independent variable.",
        "Y-Axis": "The y-axis is the vertical axis in a two-dimensional coordinate system, typically used to represent the dependent variable.",
        "Zero": "Zero is the integer that represents the absence of quantity, and it is the additive identity in arithmetic.",


    #defintions related to Computer and IT
        "Computer": "A computer is an electronic device that processes data according to instructions provided by a program. It performs calculations, stores data, and facilitates communication and automation.",
        "Central Processing Unit (CPU)": "The CPU, often called the brain of the computer, is responsible for executing instructions and performing calculations. It consists of the control unit and the arithmetic logic unit.",
        "Motherboard": "The motherboard is the main circuit board of a computer, connecting all components such as the CPU, memory, storage, and peripherals.",
        "Random Access Memory": "Random Access Memory is a type of volatile memory used to store data and instructions temporarily while a computer is running. It allows fast access to data for active tasks.",
        "RAM": "RAM is a type of volatile memory used to store data and instructions temporarily while a computer is running. It allows fast access to data for active tasks.",
        "Hard Drive": "An HDD is a storage device that uses spinning magnetic disks to store data. It provides long-term storage for files and applications.",
        "HDD": "An HDD is a storage device that uses spinning magnetic disks to store data. It provides long-term storage for files and applications.",
        "Solid-State Drive": "An SSD is a storage device that uses flash memory to store data, offering faster read and write speeds than traditional HDDs.",
        "Graphics Processing Unit": "The GPU is a specialized processor designed to handle complex graphics and image rendering, often used in gaming and professional applications.",
        "SSD": "An SSD is a storage device that uses flash memory to store data, offering faster read and write speeds than traditional HDDs.",
        "GPU": "The GPU is a specialized processor designed to handle complex graphics and image rendering, often used in gaming and professional applications.",
        "Input Device": "An input device is hardware used to provide data to a computer, such as a keyboard, mouse, microphone, or scanner.",
        "Output Device": "An output device is hardware that receives and displays or transmits information from a computer, such as a monitor, printer, or speakers.",
        "Power Supply Unit": "The PSU converts electrical power from an outlet into usable power for the internal components of a computer.",
        "Operating System": "The OS is software that manages hardware and software resources, providing a user interface and enabling application execution. Examples include Windows, macOS, and Linux.",
        "PSU": "The power supply unit converts electrical power from an outlet into usable power for the internal components of a computer.",
        "OS": "The sperating system is software that manages hardware and software resources, providing a user interface and enabling application execution. Examples include Windows, macOS, and Linux.",
        "Peripheral": "A peripheral is an external device connected to a computer, such as a printer, scanner, or external hard drive.",
        "Cache Memory": "Cache memory is a small, high-speed memory located close to the CPU, used to store frequently accessed data for faster processing.",
        "BIOS": "The BIOS is firmware that initializes hardware during startup and provides runtime services for the operating system and applications.",
        "Basic Input/Output System": "The BIOS is firmware that initializes hardware during startup and provides runtime services for the operating system and applications.",
        "Chipset": "The chipset is a collection of integrated circuits that manage data flow between the processor, memory, and peripherals.",
        "Network Interface Card": "A NIC is hardware that allows a computer to connect to a network, enabling communication with other devices.",
        "USB Port": "A USB port is a standard interface used to connect peripherals to a computer, such as flash drives, keyboards, and mice.",
        "Ethernet Port": "An Ethernet port allows a computer to connect to a wired network for internet or local area network (LAN) access.",
        "Software": "Software refers to a set of instructions or programs that enable a computer to perform specific tasks, such as operating systems and applications.",
        "Hardware": "Hardware refers to the physical components of a computer system, such as the CPU, RAM, and storage devices.",
        "Firmware": "Firmware is specialized software embedded into hardware components to control their functions, often stored in non-volatile memory.",
        "File System": "A file system organizes and stores files on a storage device, allowing users and applications to access, read, write, and manage data.",
        "Keyboard": "A keyboard is an input device used to type text and commands into a computer.",
        "Mouse": "A mouse is an input device used to interact with a computer's graphical user interface by pointing, clicking, and scrolling.",
        "Monitor": "A monitor is an output device that displays visual information generated by a computer.",
        "Webcam": "A webcam is an input device used to capture video, commonly used for video conferencing and streaming.",
        "Printer": "A printer is an output device that produces physical copies of digital documents, images, or other content.",
        "Scanner": "A scanner is an input device that converts physical documents and images into digital formats for storage or editing.",
        "CD Drive": "A CD/DVD drive is a storage device that reads and writes data to optical discs, used for media storage and playback.",
        "Bluetooth Adapter": "A Bluetooth adapter allows a computer to connect wirelessly to other devices, such as keyboards, mice, and speakers.",
        "Wi-Fi Adapter": "A Wi-Fi adapter enables a computer to connect to wireless networks for internet access and data exchange.",
        "Heat Sink": "A heat sink is a hardware component that dissipates heat generated by the CPU or GPU to prevent overheating.",
        "Cooling Fan": "A cooling fan is a device that circulates air to cool internal components of a computer and maintain optimal operating temperatures.",
        "Virtual Memory": "Virtual memory is a storage technique that uses a portion of a computer's hard drive or SSD as additional RAM when physical RAM is insufficient.",
        "Command-Line Interface": "The CLI is a text-based interface that allows users to interact with a computer by typing commands.",
        "Graphical User Interface": "A GUI is a user-friendly interface that uses visual elements like windows, icons, and menus to interact with a computer.",
        "CLI": "The CLI is a text-based interface that allows users to interact with a computer by typing commands.",
        "GUI": "A GUI is a user-friendly interface that uses visual elements like windows, icons, and menus to interact with a computer.",
        "Multitasking": "Multitasking is the ability of a computer to run multiple applications simultaneously, managed by the operating system.",

        "File": "A file is a digital container for storing data, such as documents, images, or applications.",
        "Folder": "A folder is a virtual container used to organize files on a computer for easier management and access.",
        "Backup": "A backup is a copy of data stored in a separate location to protect against loss or corruption.",
        "Firewall": "A firewall is a security system that monitors and controls incoming and outgoing network traffic to protect a computer from threats.",
        "Antivirus Software": "Antivirus software detects, prevents, and removes malicious software like viruses, worms, and spyware from a computer.",
        "Driver": "A driver is software that allows the operating system to communicate with hardware devices, such as printers and graphics cards.",
        "Boot Process": "The boot process is the sequence of events that occurs when a computer is powered on, initializing hardware and loading the operating system.",
        "SSD vs HDD": "SSDs use flash memory for faster data access, while HDDs use spinning disks and are generally slower but offer more storage for the price.",
        "Input/Output": "I/O refers to the communication between a computer and the external world, involving input from devices like keyboards and output to devices like monitors.",
        "System Unit": "The system unit is the main body of a desktop computer, housing the motherboard, CPU, RAM, and other internal components.",
        "Clock Speed": "Clock speed is the rate at which a CPU executes instructions, measured in GHz (gigahertz). Higher speeds generally mean better performance.",
        "Bus": "A bus is a communication system within a computer that transfers data between components, such as the CPU and memory.",
       
        "Algorithm": "An algorithm is a step-by-step procedure or formula for solving a problem, often used in computing and data processing.",
        "Binary Code": "Binary code is a system of representing text or computer processor instructions using the binary number system, which uses only two digits: 0 and 1.",
        "Central Processing Unit": "The CPU is the primary component of a computer that performs most of the processing inside the computer, executing instructions and performing calculations.",
        "Random Access Memory": "RAM is a type of computer memory that can be accessed randomly, allowing quick read and write access to a storage medium that is volatile in nature.",
        "CPU": "The CPU is the primary component of a computer that performs most of the processing inside the computer, executing instructions and performing calculations.",
        "RAM": "RAM is a type of computer memory that can be accessed randomly, allowing quick read and write access to a storage medium that is volatile in nature.",
    
        "Cache Memory": "Cache memory is a small, fast type of volatile computer memory that provides high-speed data access to the processor and stores frequently accessed programs and data.",
        "Simple Mail Transfer Protocol": "SMTP is a communication protocol for sending emails across the Internet, typically used to transmit messages to email servers.",
        "SMTP": "SMTP is a communication protocol for sending emails across the Internet, typically used to transmit messages to email servers.",
        "File Transfer Protocol": "FTP is a standard network protocol used to transfer files between a client and a server on a computer network.",
        "FTP": "FTP is a standard network protocol used to transfer files between a client and a server on a computer network.",
        "Transmission Control Protocol": "TCP is a core protocol of the Internet protocol suite that ensures reliable, ordered, and error-checked delivery of data between applications.",
        "TCP": "TCP is a core protocol of the Internet protocol suite that ensures reliable, ordered, and error-checked delivery of data between applications.",
        "User Datagram Protocol": "UDP is a communication protocol that provides fast but unreliable transmission of data packets, suitable for applications like video streaming and gaming.",
        "UDP": "UDP is a communication protocol that provides fast but unreliable transmission of data packets, suitable for applications like video streaming and gaming.",
        "Random Access Memory": "RAM is a type of computer memory that is volatile and used for storing data temporarily while a computer is running.",
        "RAM": "RAM is a type of computer memory that is volatile and used for storing data temporarily while a computer is running.",
        "Read-Only Memory": "ROM is a type of non-volatile memory used in computers and electronic devices to store firmware or permanent data.",
        "ROM": "ROM is a type of non-volatile memory used in computers and electronic devices to store firmware or permanent data.",
        "Central Processing Unit": "CPU is the primary component of a computer that performs most of the processing inside the system, often referred to as the brain of the computer.",
        "CPU": "CPU is the primary component of a computer that performs most of the processing inside the system, often referred to as the brain of the computer.",
        "Universal Serial Bus": "USB is a standard for connectors, cables, and communication protocols used for connection, communication, and power supply between computers and devices.",
        "USB": "USB is a standard for connectors, cables, and communication protocols used for connection, communication, and power supply between computers and devices.",
    
        "Cache Memory": "Cache memory is a small, fast type of volatile computer memory that provides high-speed data access to the processor and stores frequently accessed programs and data.",
        "Operating System": "An operating system is system software that manages hardware and software resources on a computer, providing services for computer programs.",
        "Hard Drive": "A hard drive is a data storage device used to store and retrieve digital information using magnetic storage and mechanical platters.",
        "Motherboard": "The motherboard is the primary circuit board in a computer, housing the CPU, memory, and other essential components.",
        "Input Device": "An input device is any hardware used to send data to a computer, such as a keyboard, mouse, scanner, or microphone.",
        "Output Device": "An output device is any hardware used to receive data from a computer, such as a monitor, printer, or speakers.",
        "Cloud Computing": "Cloud computing is the delivery of computing services like servers, storage, databases, and software over the internet, often offering scalable and on-demand resources.",
        "Firewall": "A firewall is a security system that monitors and controls incoming and outgoing network traffic, acting as a barrier between a trusted internal network and untrusted external networks.",
        "HyperText Transfer Protocol": "HTTP is a protocol used for transferring hypertext requests and information on the internet, enabling communication between web browsers and servers.",
        "Internet Protocol Address": "An IP address is a unique numerical label assigned to each device connected to a computer network, used to identify and locate devices on the network.",
        "Domain Name System": "DNS is a system that translates domain names (e.g., www.example.com) into IP addresses, allowing browsers to load websites using human-readable names.",
        "Hyper Text Markup Language": "HTML is the standard markup language used to create web pages, structuring content such as text, images, and links.",
        "Cascading Style Sheets": "CSS is a style sheet language used to describe the presentation of a document written in HTML, including layout, colors, and fonts.",
        "Structured Query Language": "SQL is a standard programming language used to manage and manipulate relational databases, including querying, updating, and inserting data.",

        "HTTP": "HTTP is a protocol used for transferring hypertext requests and information on the internet, enabling communication between web browsers and servers.",
        "IP Address": "An IP address is a unique numerical label assigned to each device connected to a computer network, used to identify and locate devices on the network.",
        "DNS": "DNS is a system that translates domain names (e.g., www.example.com) into IP addresses, allowing browsers to load websites using human-readable names.",
        "HTML": "HTML is the standard markup language used to create web pages, structuring content such as text, images, and links.",
        "CSS": "CSS is a style sheet language used to describe the presentation of a document written in HTML, including layout, colors, and fonts.",
        "SQL": "SQL is a standard programming language used to manage and manipulate relational databases, including querying, updating, and inserting data.",
   
        "JavaScript": "JavaScript is a programming language used to create dynamic and interactive effects on web pages, such as animations, form validation, and interactive elements.",
        "Database": "A database is an organized collection of data, typically stored and accessed electronically from a computer system, used for data management and retrieval.",
        "Encryption": "Encryption is the process of converting data into a coded format to prevent unauthorized access, ensuring privacy and data security.",
        "Decryption": "Decryption is the process of converting encrypted data back into its original form using an algorithm and a key.",
        "Python": "Python is a high-level, interpreted programming language known for its simplicity and readability, used in web development, data science, artificial intelligence, and more.",
        "Java": "Java is a general-purpose, object-oriented programming language used in web applications, software development, and mobile app development.",
        "C++": "C++ is a programming language that extends C by adding object-oriented features, widely used in system software, game development, and high-performance applications.",
        "JavaScript": "JavaScript is a versatile programming language primarily used in web development to create interactive and dynamic web pages.",
        "Ruby": "Ruby is a high-level, interpreted programming language known for its simplicity and productivity, often used in web development through the Ruby on Rails framework.",
        "PHP": "PHP is a server-side scripting language designed for web development, allowing dynamic content to be generated and integrated into web pages.",
        "Swift": "Swift is a programming language developed by Apple for creating applications for iOS, macOS, and other Apple platforms.",
        "Assembly Language": "Assembly language is a low-level programming language that is closely related to machine code and is used for programming directly in a computer's hardware.",
        "Compiler": "A compiler is a program that translates high-level programming code into machine language that a computer can execute.",
        "Interpreter": "An interpreter is a program that reads and executes code line by line, without converting it into machine code beforehand, useful for scripting languages.",
        "API": "An Application Programming Interface (API) is a set of rules and protocols that allow different software applications to communicate and share data with each other.",
        "IDE": "An Integrated Development Environment (IDE) is a software application that provides developers with tools to write, test, and debug their code, including a code editor, compiler, and debugger.",
        "Version Control": "Version control is a system that manages changes to files, allowing multiple developers to track and manage changes in software development.",
        "Git": "Git is a distributed version control system that allows multiple developers to collaborate on software development by tracking changes to files.",
        "GitHub": "GitHub is a web-based platform for version control and collaboration, where developers can host and share their code using Git.",
        "Cloud Storage": "Cloud storage is a service that allows users to store data on remote servers accessible via the internet, providing scalability and accessibility.",
        "Bit": "A bit is the smallest unit of data in computing, representing a binary value of 0 or 1.",
        "Byte": "A byte is a unit of digital information consisting of 8 bits, often used to represent a character in a computer's memory.",
        "Operating System Kernel": "The kernel is the core part of an operating system, managing system resources, hardware communication, and facilitating software execution.",
        "Multitasking": "Multitasking is the ability of an operating system to execute multiple tasks or processes simultaneously, often by switching between them rapidly.",
        "Process": "A process is an instance of a program that is being executed by the operating system, consisting of the program code, data, and system resources.",
        "Thread": "A thread is the smallest unit of execution within a process, allowing a program to perform multiple tasks concurrently.",
        "Virtual Memory": "Virtual memory is a memory management technique that uses both physical RAM and disk space to simulate a larger memory capacity than physically available.",
        "Hard Disk": "A hard disk is a non-volatile storage device used to store data permanently, utilizing magnetic storage technology for long-term data retention.",
        "Machine Learning": "Machine learning is a type of artificial intelligence that allows computers to learn from data and improve their performance on tasks without explicit programming.",
        "Artificial Intelligence": "Artificial intelligence (AI) is the simulation of human intelligence in machines that are programmed to think and learn like humans.",
        "Neural Network": "A neural network is a computational model inspired by the human brain, used in machine learning for pattern recognition and decision making.",
        "Deep Learning": "Deep learning is a subset of machine learning that uses neural networks with many layers to analyze large amounts of data and solve complex tasks.",
        "Natural Language Processing (NLP)": "NLP is a field of artificial intelligence that focuses on the interaction between computers and human language, enabling machines to understand, interpret, and generate natural language.",
        "Computer Vision": "Computer vision is a field of artificial intelligence that enables computers to interpret and make decisions based on visual data, such as images or video.",
        "Big Data": "Big data refers to large and complex datasets that require advanced tools and technologies to store, manage, and analyze.",
        "Blockchain": "Blockchain is a decentralized digital ledger technology that securely records transactions across multiple computers, preventing tampering and fraud.",
        "Cryptocurrency": "Cryptocurrency is a type of digital currency that uses cryptography for secure financial transactions and operates independently of a central bank.",
        "Cybersecurity": "Cybersecurity is the practice of protecting computers, networks, and data from unauthorized access, attacks, or damage.",
        "Phishing": "Phishing is a type of cyber attack in which attackers deceive users into providing sensitive information, such as passwords or credit card details, often via email or fake websites.",
        "Malware": "Malware is malicious software designed to damage, disrupt, or gain unauthorized access to a computer system or network.",
        "Ransomware": "Ransomware is a type of malware that encrypts a user's data and demands payment for the decryption key.",
        "Spyware": "Spyware is a type of malicious software that secretly monitors and collects user data without their knowledge or consent.",
        "Firewall": "A firewall is a security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.",
        "Cloud Security": "Cloud security refers to the measures taken to protect data, applications, and infrastructures involved in cloud computing from cyber threats.",
        "Virtual Private Network (VPN)": "A VPN is a service that encrypts your internet connection and hides your IP address, providing secure and private online communication.",
        "Two-Factor Authentication (2FA)": "2FA is an additional layer of security that requires users to provide two forms of identification before accessing a system or account.",
        "Authentication": "Authentication is the process of verifying the identity of a user or system, often through passwords, biometrics, or security tokens.",
        "Authorization": "Authorization is the process of granting or denying access to resources based on the authenticated identity and permissions.",
        "Data Encryption": "Data encryption is the process of converting plain text into a coded format to prevent unauthorized access during transmission or storage.",
        "Hashing": "Hashing is a cryptographic process that converts data into a fixed-length string, often used for data integrity and password storage.",
        "Artificial Neural Network": "An Artificial Neural Network is a type of machine learning model inspired by biological neural networks, consisting of interconnected nodes that process data.",
        "Cloud Infrastructure": "Cloud infrastructure refers to the physical and virtual resources required to support cloud computing, including servers, storage, and networking components.",
        "Data Mining": "Data mining is the process of discovering patterns and insights from large datasets using statistical, mathematical, and machine learning techniques.",
        "Relational Database": "A relational database is a type of database that stores data in structured tables with predefined relationships between them.",
        "Primary Key": "A primary key is a unique identifier for a record in a relational database table, ensuring that no two records are identical.",
        "Foreign Key": "A foreign key is a field in a database table that establishes a link between two tables by referencing the primary key in another table.",
        "Normalization": "Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity.",
        "Denormalization": "Denormalization is the process of combining normalized database tables to improve read performance by reducing the number of joins needed for queries.",
        "Big-O Notation": "Big-O notation is a mathematical representation used in computer science to describe the efficiency of algorithms in terms of time or space complexity.",
        "Data Structure": "A data structure is a way of organizing and storing data in a computer so that it can be accessed and used efficiently.",
        "Array": "An array is a collection of elements, usually of the same type, stored in contiguous memory locations and accessed using an index.",
        "Linked List": "A linked list is a linear data structure in which elements are stored in nodes that are linked together using pointers.",
        "Stack": "A stack is a linear data structure that follows the Last In, First Out (LIFO) principle, where the last element added is the first to be removed.",
        "Queue": "A queue is a linear data structure that follows the First In, First Out (FIFO) principle, where the first element added is the first to be removed.",
        "Hash Table": "A hash table is a data structure that uses a hash function to map keys to values, enabling fast data retrieval.",
        "Binary Tree": "A binary tree is a hierarchical data structure in which each node has at most two child nodes, often referred to as left and right children.",
        "Graph": "A graph is a collection of nodes (vertices) connected by edges, used to represent relationships between elements.",
        "Breadth-First Search (BFS)": "BFS is an algorithm for traversing or searching graph data structures by exploring all neighbors at the current depth before moving to the next level.",
        "Depth-First Search (DFS)": "DFS is an algorithm for traversing or searching graph data structures by exploring as far as possible along each branch before backtracking.",
        "Cloud Backup": "Cloud backup is a service that allows users to store and protect data by creating copies in cloud storage systems.",
        "Network Protocol": "A network protocol is a set of rules and conventions that govern how data is transmitted and received over a network.",
        "TCP/IP": "TCP/IP is a suite of communication protocols used to interconnect network devices on the internet, consisting of the Transmission Control Protocol and Internet Protocol.",
        "Ethernet": "Ethernet is a family of networking technologies commonly used in local area networks (LANs), providing high-speed data communication.",
        "Packet": "A packet is a unit of data that is transmitted over a network, containing both the data payload and control information like headers.",
        "Switch": "A switch is a network device that connects multiple devices and uses MAC addresses to forward data to the correct destination.",
        "Router": "A router is a device that connects multiple networks and directs data packets to their intended destinations using IP addresses.",
        "IoT": "IoT refers to the network of physical devices embedded with sensors, software, and connectivity to exchange data over the internet.",
        "Machine Code": "Machine code is a low-level programming language consisting of binary instructions that a computer's CPU can execute directly.",
        "Assembly Language": "Assembly language is a human-readable representation of machine code, often used for low-level hardware programming.",
        "Compiler Optimization": "Compiler optimization is the process of improving the performance and efficiency of compiled code by removing redundancies and reorganizing instructions.",
        "Thread Scheduling": "Thread scheduling is the process of managing the execution of multiple threads on a CPU, ensuring efficient use of resources.",
        "Peer-to-Peer Network": "A peer-to-peer network is a decentralized network where devices (peers) share resources directly without relying on a central server.",
        "Distributed System": "A distributed system is a network of independent computers that work together to perform a task, appearing as a single system to users.",
        "Load Balancing": "Load balancing is the process of distributing workloads across multiple servers or resources to ensure efficiency and prevent overloading.",
        "Virtual Machine": "A virtual machine is a software-based emulation of a computer system, allowing multiple operating systems to run on a single physical machine.",
        "Open Source Software": "Open source software is software with source code that anyone can inspect, modify, and enhance.",
        "Proprietary Software": "Proprietary software is software that is privately owned, and its source code is not available for public modification or redistribution.",
        "Cloud Platform as a Service (PaaS)": "PaaS is a cloud computing service that provides a platform allowing developers to build, deploy, and manage applications without dealing with infrastructure complexities.",
        "Cloud Infrastructure as a Service (IaaS)": "IaaS is a cloud computing service that provides virtualized computing resources like servers, storage, and networking over the internet.",
        "Blockchain Node": "A blockchain node is a device or program that maintains a copy of the blockchain and participates in the network's operations, such as validating transactions.",
        "Digital Signature": "A digital signature is a cryptographic technique used to verify the authenticity and integrity of digital data, ensuring it has not been altered.",
        "Data Redundancy": "Data redundancy is the duplication of data in a database or storage system to improve reliability and data recovery in case of failure.",
        "Network Latency": "Network latency is the time delay experienced in data communication over a network, often measured in milliseconds.",
        "Ping": "Ping is a diagnostic tool used to test the connectivity and latency between two devices on a network.",
        "Blockchain Consensus Algorithm": "A blockchain consensus algorithm is a protocol that ensures all nodes in a blockchain network agree on the state of the distributed ledger.",
        "Smart Contract": "A smart contract is a self-executing program stored on a blockchain that automatically enforces and executes the terms of an agreement.",
        "DNS Server": "A DNS server is a server that translates domain names into IP addresses, enabling devices to locate websites and services on the internet.",
        "Quality of Service": "QoS refers to the techniques used to prioritize and manage network traffic, ensuring reliable performance for critical applications.",
        "Malware Analysis": "Malware analysis is the process of examining malicious software to understand its behavior, functionality, and impact on systems.",
        "Botnet": "A botnet is a network of compromised computers controlled by an attacker, often used to launch coordinated cyberattacks like DDoS.",
        "Virtualization": "Virtualization is the process of creating virtual versions of physical resources, such as servers, storage, or networks, for better efficiency and scalability.",
        "Hypervisor": "A hypervisor is software that creates and manages virtual machines, allowing multiple operating systems to run on a single physical machine.",
        "Biometrics": "Biometrics refers to the use of physical or behavioral characteristics, such as fingerprints or voice patterns, for identity verification and authentication."

    }


    for topic in science_definitions.keys():
        if f"define {topic}".lower() in command.lower() or f"definition of {topic}".lower() in command.lower():
            
            definition = science_definitions[topic]
            talk(f"{topic}: {definition}")
            break

        elif topic not in science_definitions.keys():
            talk('The topic is not included in my database.')        
            




#_______________________________________
#| PART- TWO: THE TRANSLATION SECTION: |
#--------------------------------------|
 
    # some common languages
    language_map = {
      "english": "en",
      "spanish": "es",
      "french": "fr",
      "german": "de",
      "urdu": "ur", 
      "chinese": "zh",
      "hindi": "hi",}

    try:
        if "translate" in command and "to" in command:
            parts = command.split(" to ")

            if len(parts) < 2:
                talk("Please use the format: 'translate [text] to [language]'.")
            else:
                text_to_translate = parts[0].replace("translate ", "").strip()
                target_language = parts[1].strip()

            language_code = language_map.get(target_language.lower())


            if not language_code:
                talk(f"Sorry, I don't recognize the language '{target_language}'. Please try again.")
            else:
                try:
                    translated = translator.translate(text_to_translate, dest=language_code)
                    talk(f"Translation to {target_language.capitalize()}: {translated.text}")
                except Exception as e:
                    talk("There was an error with the translation service. Please try again.")

    except Exception as e:
        talk("There was an error with your request. Please use the format: 'translate [text] to [language]'.")
        print(f"Error: {str(e)}")



#______________________________________
#| PART- SIX: SEND WHATSAPP MESSAGES: |
#-------------------------------------|

    def load_contacts(file_name = "contacts.txt"):
        contacts = {}
        with open(file_name, 'r') as file:
            for line in file:
                name, phone = line.strip().split(", ")
                contacts[name.lower()] = phone
            return contacts


    try:
        sm_variations = ['send a message to', 'send message to', 'send whatsapp message to', 'send whatsapp to', 'send a text to']
        for variation in sm_variations:
        
        #sending message right now
            if variation in command and 'saying that' in command:
                command = command.replace("now", "")
                command = command.replace(variation, "")

                parts = command.split(' saying that ')
                contact_name = parts[0].lower().strip()
                message = parts[1].strip()
                message =  message + " \n ________________________________________________________________________________ \n MESSAGE SENT BY DODO-AI \n ________________________________________________________________________________ " 

                contacts = load_contacts()

                if contact_name in contacts:
                    contact_number = contacts[contact_name]
                    talk(f"Sending your message to {contact_name}.")
                    
                    now = datetime.datetime.now() + datetime.timedelta(minutes=1)
                    time_hour = now.hour
                    time_minute = now.minute
                    pywhatkit.sendwhatmsg(contact_number, message, time_hour, time_minute)

                    talk(f"Sir I have successfully sent your message to {contact_name}.")
                
                else:
                    talk(f"Sorry, I couldn't find {contact_name} in your contacts. Please check the name and try again.")
                    break

      #send a message a specific time,,, will also write that code here too

    except Exception as e:
        talk(f"Sorry, I couldn't send the message due to an error.")
        print(f"Error: {e}")



#___________________________________________
#| PART- SEVEN: SEARCHING ON SOCIAL MEDIA: |
#------------------------------------------|
    try:
        search_variations = ['can you find', 'can you search for', 'can you look for', 'search for', 'find', 'look for', 'search']
        for variation in search_variations:
        
        #searching on Facebook
            if variation in command and "facebook" in command:
                command = command.replace(variation, '')
                parts = command.split(' on ')

                person_to_search = parts[0].strip().lower().capitalize()
                
                talk(f"Sir, I am searching for {person_to_search} on Google with Facebook results.")
                search_url = f"https://www.google.com/search?q=site:facebook.com+{person_to_search}"

                webbrowser.open(search_url)
                talk("Sir, this is what I found based on your request.")
                break
        
        #searching on Instagram
            if variation in command and "instagram" in command:
                command = command.replace(variation, '')
                parts = command.split(' on ')

                person_to_search = parts[0].strip().lower().capitalize()
                
                talk(f"Sir, I am searching for {person_to_search} on Google with Instagram results.")
                search_url = f"https://www.google.com/search?q=site:instagram.com+{person_to_search}"

                webbrowser.open(search_url)
                talk("Sir, this is what I found based on your request.")
                break
        
        #searching on Tiktok
            if variation in command and "tiktok" in command:
                command = command.replace(variation, '')
                parts = command.split(' on ')

                person_to_search = parts[0].strip().lower().capitalize()
                
                talk(f"Sir, I am searching for {person_to_search} on Google with Tiktok results.")
                search_url = f"https://www.google.com/search?q=site:tiktok.com+{person_to_search}"

                webbrowser.open(search_url)
                talk("Sir, this is what I found based on your request.")
                break
        
        #searching on Linkedin
            if variation in command and "linkedin" in command:
                command = command.replace(variation, '')
                parts = command.split(' on ')

                person_to_search = parts[0].strip().lower().capitalize()
                
                talk(f"Sir, I am searching for {person_to_search} on Google with LinkedIn results.")
                search_url = f"https://www.google.com/search?q=site:linkedin.com+{person_to_search}"

                webbrowser.open(search_url)
                talk("Sir, this is what I found based on your request.")
                break

        #searching on Twitter
            if variation in command and "twitter" in command:
                command = command.replace(variation, '')
                parts = command.split(' on ')

                person_to_search = parts[0].strip().lower().capitalize()
                
                talk(f"Sir, I am searching for {person_to_search} on Google with Twitter results.")
                search_url = f"https://www.google.com/search?q=site:twitter.com+{person_to_search}"

                webbrowser.open(search_url)
                talk("Sir, this is what I found based on your request.")
                break
    except Exception as e:
        talk(f"Sorry, I couldn't perform the search.")
        print(f"Error: {e}")



#_______________________________________
#| PART- EIGHT: CLEARING THE TERMINAL: |
#--------------------------------------|

    try:
        clear_variations = ['clear', 'clean', 'remove']
        for variation in clear_variations:
            if variation in command and 'terminal' in command or 'screen' in command:
                talk('Sir, I am clearing the Terminal on your request.')
                os.system('cls' if os.name == 'nt' else 'clear')
                break
    
    except Exception as e:
        talk('Sir, there was an error while clearing the terminal')
        print(f"Error: {e}")



#________________________________
#| PART- NINE: FILE MANAGEMENT: |
#-------------------------------|

 #Functions for file managment#
  #1. Listing Function
    def list_files():
        files = os.listdir('.')
        if files:
            talk("Sir, here are the files and folders in the current directory:")
            for file in files:
                print("  => "+file)
            talk("Sir, I have displayed the list in the terminal.")
        else:
            talk("Sir, the directory is empty.")

  #2. Folder Creating Function
    def create_folder(folder_name):
        try:
            os.mkdir(folder_name)
            talk(f"Sir, folder '{folder_name}' has been created.")
        except FileExistsError:
            talk(f"Sir, a folder named '{folder_name}' already exists.")
        except Exception as e:
            talk(f"Sir, I couldn't make the folder.")
            print(f"Error:{e}")

   #3. File Opening Function
    def open_item(item_name):
        try:
         # Get the current working directory
         current_directory = os.getcwd()

        # Build the full path to the target item
         target_path = os.path.join(current_directory, item_name)

        # Check if the item exists
         if os.path.exists(target_path):
            if os.path.isdir(target_path):
                # Open a folder
                os.startfile(target_path)  # Works on Windows
                talk(f"I am opening the folder {item_name}, sir.")
            elif os.path.isfile(target_path):
                # Open a file
                subprocess.run(['open', target_path], check=True)  # Works on macOS and Linux
                talk(f"I am opening the file {item_name}, sir.")
         else:
            talk(f"Sorry, I couldn't find {item_name}. Please check the name and try again.")
        except Exception as e:
         talk(f"An error occurred: {str(e)}")



  #for navigating to a folder

  #for listing the components of a folder
    try:
        listing_variations = ['list', 'show', 'see']
        for variation in listing_variations:
            if variation in command and 'folders' in command or 'file' in command or 'components' in command or 'directories' in command or 'directory' in command:
             list_files()
             break
    except Exception as e:
        talk('Sir, there was an error while showing the list.')
        print(f"Error: {e}") 



    #create a folder named my books
  #for creating a folder 
    try:
        create_variations = ['create', 'make', 'build', 'craft', 'contruct', 'generate', 'develop', 'design']
        for variation in create_variations:
            if variation in command and 'folder' in command or 'directory' in command and 'nam' in command:
             parts = command.split(' named ')
             folder_name = parts[1].strip()
             create_folder(folder_name)
             break
    except Exception as e:
        talk('Sir, there was an error while creating a folder.')
        print(f"Error: {e}") 

  #for opening a file
    try:
        open_variations = ['play']
        for variation in open_variations:
            if variation in command:
             item_name = command.replace(variation, '').strip()
             print(item_name)
             open_item(item_name)
             break
    except Exception as e:
        talk('Sir, there was an error while opening your file.')
        print(f"Error: {e}") 

  #for deleting a folder













#_________________________________________
#| PART- THREE: THE MATHEMATICS SECTION: |
#----------------------------------------|

    try:
     if 'can you help me with math' in command or 'can you do math' in command or 'can you help with with mathematics' in command:
        text = 'Of course! I can help you with your basic Mathematics including addition, subtraction, multiplication and division. What math problem do you have?'
        talk(text)

    # Check for addition
     if 'plus' in command or 'add' in command or '+' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        result = sum(numbers)
        talk(f"The result of your addition is: {result}.")

     # Check for subtraction
     elif 'minus' in command or 'subtract' in command or '-' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        result = numbers[0] - numbers[1]
        talk(f"The result of your subtraction is: {result}.")

    #Check for multiplication
     elif 'multiply' in command or 'times' in command or '*' in command or 'x' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        result = numbers[0] * numbers[1]
        talk(f"The result of your multiplication is: {result}.")

    # Check for division
     elif 'divide' in command or 'divided by' in command or '/' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        if numbers[1] == 0:
                talk("Division by zero is undefined.")
        result = numbers[0] / numbers[1]
        talk(f"The result of your division is: {result}.")
    
    #Check for square of a number
     elif 'square of' in command or 'squared' in command:
        number = [int(num) for num in re.findall(r'\d+', command)]
        result = number[0]*number[0]
        talk(f"Your result will be: {result}.") 


    #Check for average
     elif 'average of' in command or 'mean of ' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        result = sum(numbers) / len(numbers)
        talk(f"The average of the numbers is {result}.")

    #Check for percentage calculation
     elif 'percent of' in command or 'percent out of' in command or 'percentage of' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        if len(numbers) == 2:
            result = (numbers[0] / 100) * numbers[1]
            talk(f"Your answer is: {result}%")

    #Check for square root
     elif 'square root of' in command:
        numbers = [int(num) for num in re.findall(r'\d+', command)]
        if numbers[0] < 0:
            talk("Sorry, square root of a negative number is not a real number.")
        result = numbers[0] ** 0.5
        talk(f"The square root of {numbers[0]} is: {result}.")

    except Exception as e:
        talk("Sorry, I couldn't understand your problem. Please rephrase.")
        print(f"Error: {e}")



#__________________________________________
#| PART- FOUR: THE ENTERTAINMENT SECTION: |
#-----------------------------------------|
    if 'my mood is off' in command or 'i am feeling unwell' in command or 'i am not feeling good' in command or 'i am feeling low' in command:
        text = "Well, I'm really sorry you're feeling this way, but I'm glad you reached out. It can be tough, and it's okay to have moments when" \
               " things feel heavy. If you'd like, I can try to make you feel better. Choose one of the followings:, \n 1. Playing a song of your favorite singer \n 2. Telling me a story \n 3. Say some jokes \n 4. Say some poetry for me \n 5. Tell me a fun fact \n 6. Play a movie on Youtube"
        talk(text)

#Playing of Song:
    try:
     play_song_variations = ['play song of', 'play music of', 'play a song of','play a song', 'play the song', 'play a music of','play the music', 'play the music of', 'play the song of', 'play song', 'play music', 'play some song', 'play some music']
     for variation in play_song_variations:
        if variation in command:
            song = command.replace(variation, '')
            talk('Playing the song of ' + song)
            pywhatkit.playonyt(song)
            break
    except:
       talk("To play a music first please say, 'Play a song of', then add your favorite singer or artist name or even the song name itself.")

    try:
     play_movie_variations = ['play movie of', 'play the movie of', 'play a movie of','play a movie', 'play a film', 'play a film of', 'play the movie',
                              'play the film', 'play the film of', 'play movie', 'play film', 'play some movie', 'play some film']
     for variation in play_movie_variations:
        if variation in command:
            movie1 = command.replace(variation, '').strip()
            movie2 = "Movie of " + movie1
            talk('Playing movie of ' + movie1)
            pywhatkit.playonyt(movie2)
            break
    except:
       talk("Try again with different movie name.")

    try:
     play_news_variations = ['play']
     for variation in play_news_variations:
        if variation in command and 'news' in command:

            news1 = command.replace(variation, '')
            news2 = news1.replace("news", "")
            news3 = news2.replace('live', "")
            news_play = news3.upper().strip()

            talk(f"Sir, playing {news_play} News for you.")
            pywhatkit.playonyt(news_play + "live")
            break
    except Exception as e:
       talk("Try again with different news channel name.")
       print(f"Error: {e}")


#Telling a Story:
    if 'tell me a story' in command or 'story me' in command or 'another story' in command:
        talk("What type of story you want to listen?. Some suggestions are inspiring stories, fairy tales, or stories for kids, if you are one.")

    stories = {
            "inspiring_stories": [
                "Thomas Edison failed over 1,000 times before inventing the lightbulb, but he never gave up. His perseverance and determination changed the world, proving that failure is just a stepping stone to success.",
                "J.K. Rowling, the author of the Harry Potter series, was rejected by 12 publishers before finding success. Her story reminds us that persistence is key, and even rejection can lead to greatness.",
                "Steve Jobs was fired from the company he co-founded, Apple, only to return and lead it to become one of the most successful businesses in the world. His story is one of resilience, innovation, and vision.",
                "Walt Disney was told he lacked creativity and was rejected by many before creating Disney. He believed in his dream and became one of the most iconic entrepreneurs in history.",
                "Oprah Winfrey faced many hardships in her early life, including poverty and abuse, but she overcame them to become one of the most influential media personalities of all time. Her story teaches us the power of perseverance and self-belief.",
                "Richard Branson, the founder of Virgin, started with no formal education but used his creativity and determination to build a global empire that spans multiple industries, showing that success is not bound by traditional norms.",
                "Bethany Hamilton, a surfer who lost her arm in a shark attack, continued surfing professionally and became an inspiration to many, showing that courage and resilience can overcome the toughest challenges.",
                "Henry Ford revolutionized the automobile industry with the Model T, making cars affordable for the average person. His perseverance and vision turned a simple idea into a global phenomenon.",
                "Warren, a young boy from a small village, dreamed of becoming an astronaut. Despite many naysayers, he studied relentlessly and worked hard to join the space program, becoming the youngest astronaut to travel to space and inspiring millions of children worldwide.",
                "Lucas, a young inventor, spent years building a flying machine in his garage. After multiple failed attempts, he finally succeeded and became the first person to invent a plane capable of vertical take-off, revolutionizing air travel for the future.",
                "Emily, a gifted musician, had her compositions rejected by countless record labels. Instead of giving up, she started her own music production company, and her unique sound went on to inspire the next generation of musicians.",
                "Amira, a skilled engineer from a remote village, designed a sustainable energy solution that provided electricity to her community. Her determination and creativity transformed her village, and her innovation caught the attention of global tech companies.",
                "Victor, a young inventor, created a machine that could clean the oceans of plastic waste. Though many doubted his invention, his machine became the standard for environmental cleanup, saving marine life and restoring ecosystems around the world.",
                "Riley, a determined young woman, faced every challenge to become the first female firefighter in her city. After years of training and perseverance, she earned respect and admiration, opening doors for women in the male-dominated field of firefighting.",
                "Kai, a self-taught coder, built a mobile app that helped people with disabilities communicate more effectively. His invention gained global recognition and became a lifeline for thousands of people, proving that anyone can create positive change.",
                "Lana, a young artist with no formal training, painted a series of portraits that showcased the beauty of diverse cultures. Her work was exhibited worldwide, and she became a champion of cultural diversity in the art world.",
                "In a small coastal town, a teenager named Isaac was determined to stop the destruction of the coral reefs. He started a campaign, raised awareness, and worked with scientists to develop solutions, ultimately saving the reefs and inspiring a global conservation movement.",
                "Natalie, a single mother, worked three jobs to support her family while pursuing her dream of becoming a lawyer. After years of hard work, she graduated top of her class and became an advocate for families in need of legal representation.",
                "Mason, a young chef with a passion for food, was turned down by many restaurants. Instead of quitting, he opened his own restaurant, which became a culinary sensation and earned him accolades as one of the best chefs in the world.",
                "Ella, a determined young woman with no formal education, taught herself to program and created a successful tech startup that provided affordable learning tools to underserved communities, transforming the educational landscape.",
                "Jason, a young athlete, overcame a serious injury that threatened to end his career. With relentless rehab and mental strength, he not only returned to the sport but went on to win multiple national championships, proving that strength lies in resilience.",
                "Lucas, an aspiring archaeologist, had no funding for his digs. Instead of giving up, he used crowd-funding to finance his expeditions and uncovered ancient treasures that provided valuable insights into the early civilizations.",
                "Amara, a young environmentalist, spent years campaigning to reduce the use of plastic. Her tireless advocacy led to the passing of several laws worldwide that reduced plastic waste, changing how industries approach sustainability."],

            "kids_stories": [
                "The Three Little Pigs: Once upon a time, there were three little pigs who left home to build their own houses. The first pig built a house of straw, but a big bad wolf blew it down. The second pig built a house of sticks, but the wolf blew that down too. The third pig built a strong house of bricks. The wolf tried and tried but couldn’t blow it down. The three pigs lived happily ever after, safe and sound in the brick house.",
                "Goldilocks and the Three Bears: Goldilocks, a curious girl, wandered into the forest and found a house belonging to three bears. She tasted their porridge, sat in their chairs, and even slept in their beds. The bears came home and found Goldilocks in their house. She woke up and ran away, never to return. The bears learned to keep their doors locked from then on.",
                "The Little Red Hen: One day, the little red hen found some wheat seeds and decided to plant them. She asked her friends, the cat, the dog, and the duck, for help, but they all refused. She planted, watered, and harvested the wheat by herself. When it was time to make bread, her friends still refused to help. So, she baked the bread and ate it all herself, teaching her friends the value of hard work.",
                "The Ant and the Grasshopper: During the summer, the ant worked hard to gather food for the winter, while the grasshopper sang and played. When winter came, the grasshopper had no food and asked the ant for help. The ant refused, teaching the grasshopper the importance of planning and hard work.",
                "The Lion and the Mouse: A lion caught a little mouse and was about to eat him. The mouse begged for mercy, promising to help the lion someday. The lion laughed but let the mouse go. Later, the lion was trapped in a net, and the mouse chewed through the ropes to set him free. The lion learned that even the smallest creatures can be helpful.",
                "The Ugly Duckling: An ugly duckling was born into a family of beautiful ducks. He was teased and rejected by the other animals. As he grew older, he discovered he was actually a beautiful swan. The other animals admired him, and he was no longer lonely. The story teaches that true beauty comes from within.",
                "The Tortoise and the Hare: The hare was very proud of how fast he could run, so he challenged the slow-moving tortoise to a race. Confident that he would win, the hare took a nap during the race. Meanwhile, the tortoise kept going steadily and won the race. The story teaches the lesson that slow and steady wins the race.",
                "The Gingerbread Man: An old woman baked a gingerbread man who jumped out of the oven and ran away. He outran the woman, the man, and many animals, taunting them with his speed. But when he met a fox, the fox tricked him into climbing onto his back, and the gingerbread man was eaten. The story is a fun reminder about the consequences of being too confident.",
                "The Velveteen Rabbit: A stuffed rabbit wanted to become real by being loved. Over time, the rabbit was loved and played with by a child, and he became real through their love. One day, the child fell ill, and the rabbit was thrown away, but he was later transformed into a real rabbit and lived a joyful life, having been loved so much.",
                "The Boy Who Cried Wolf: A young shepherd boy repeatedly cried out that a wolf was attacking his sheep, even though it wasn’t true. One day, a wolf really came, but when the boy cried for help, no one believed him. The wolf ate the sheep, teaching the boy the importance of telling the truth."],

            "fairy_tales" : [
                "Cinderella: Once upon a time, there was a kind and beautiful girl named Cinderella who lived with her wicked stepmother and two cruel stepsisters. They treated her as a servant, making her do all the chores while they enjoyed a life of luxury. Despite their cruelty, Cinderella remained kind and hopeful. One day, the king announced a grand ball to find a bride for the prince. The stepsisters excitedly prepared for the ball, but Cinderella was told she couldn’t attend. As she cried in despair, her Fairy Godmother appeared. Using her magic, the Fairy Godmother transformed a pumpkin into a magnificent carriage, mice into horses, and Cinderella's rags into a stunning gown with glass slippers. However, the magic would only last until midnight. At the ball, everyone was captivated by Cinderella’s beauty, including the prince. They danced the night away, and Cinderella felt like a dream had come true. However, as the clock struck midnight, she had to flee, leaving behind one of her glass slippers. The prince, determined to find the mysterious girl, searched the kingdom with the glass slipper. Every young woman tried it on, but it fit none until Cinderella stepped forward. Her stepsisters mocked her, but when the slipper fit perfectly, they were silenced. Cinderella married the prince and forgave her stepfamily. They lived happily ever after, proving that kindness and hope can overcome any hardship.",
                "Snow White and the Seven Dwarfs: Snow White was a princess, the daughter of a kind and beautiful queen. But when the queen died, her father remarried a wicked woman who was jealous of Snow White's beauty. The queen’s magic mirror told her that Snow White was the fairest of them all, which made the queen furious. She ordered a huntsman to take Snow White into the forest and kill her. However, the huntsman couldn’t bring himself to harm the girl and let her go. Snow White wandered deep into the forest and found a cottage where seven dwarfs lived. The dwarfs took her in and warned her to be careful of the queen. Meanwhile, the queen, learning that Snow White was still alive, disguised herself as an old woman and gave Snow White a poisoned apple. Snow White took a bite and fell into a deep, enchanted sleep. The dwarfs were heartbroken and placed her in a glass coffin. A prince who had heard of Snow White’s beauty and kindness arrived and kissed her. Snow White woke up, and they were married. The wicked queen, upon hearing of Snow White’s happiness, was consumed with rage and punished for her wickedness. Snow White and the prince lived happily ever after.",
                "Beauty and the Beast: A wealthy merchant had three daughters, and the youngest, named Belle, was the most beautiful and kind-hearted. One day, the merchant lost his fortune and went to a faraway town to find work. On the way, he was lost in the woods and stumbled upon a mysterious castle. He took a rose from the garden to give to Belle, but a Beast, who lived in the castle, appeared and demanded that the merchant pay the price for picking the rose. The merchant offered to trade his life for the rose, but the Beast allowed him to go if he promised to return. The merchant returned to the Beast, and Belle, wanting to save her father, agreed to stay in his place. Over time, Belle learned that the Beast was kind-hearted and misunderstood. She grew fond of him, and when she realized that she loved him, the Beast was transformed back into a prince, breaking the curse that had been placed on him. Belle and the prince married, and they lived happily ever after.",
                "Rapunzel: A couple lived next to a garden owned by a wicked witch. When the wife became pregnant, she longed for the rapunzel plants from the witch’s garden. Her husband stole some, and the witch caught him. She agreed not to harm him but demanded their baby as payment. The baby, a girl named Rapunzel, grew up to be incredibly beautiful, and the witch locked her in a tower with no stairs or door. One day, a prince heard Rapunzel singing and found the tower. They began meeting secretly, and eventually, Rapunzel agreed to run away with him. The witch found out and, in a fit of rage, cast Rapunzel into the wilderness. The prince, heartbroken, wandered blind until Rapunzel found him. Her tears of joy healed his eyes, and they were married. Rapunzel and the prince lived happily ever after, free from the witch’s cruelty.",
                "Little Red Riding Hood: Once upon a time, a sweet little girl named Little Red Riding Hood was sent by her mother to visit her grandmother in the woods. Her mother warned her not to stray from the path. However, along the way, Little Red Riding Hood met a wolf, who tricked her into revealing where her grandmother lived. The wolf ran ahead and disguised himself as the grandmother, waiting for Little Red Riding Hood. When she arrived, she noticed the strange appearance of her 'grandmother' but was too late. The wolf lunged at her, but a passing huntsman heard the noise and rushed to save them both. He killed the wolf and saved the grandmother. Little Red Riding Hood learned to always be cautious and never stray from the path.",
                "Hansel and Gretel: Hansel and Gretel were siblings who were abandoned in the woods by their wicked stepmother and father. They wandered through the forest until they found a house made of candy. The witch who lived there lured them inside and locked Hansel in a cage to fatten him up, planning to eat him. Gretel, however, managed to trick the witch and pushed her into the oven, killing her. Hansel and Gretel escaped with the witch’s treasure and returned home. Their father, who regretted his actions, welcomed them back with open arms, and they lived happily ever after.",
                "The Frog Prince: A spoiled princess was playing with a golden ball by a pond when it fell into the water. A frog offered to retrieve the ball if she promised to let him live with her and be her companion. She agreed, but when the frog brought her ball back, she refused to keep her promise. The frog insisted, and when the princess finally let him into her home, he transformed into a handsome prince. The prince explained that he had been cursed by a wicked witch, and the curse was broken by her kindness. The princess and the prince fell in love and were married, living happily ever after.",
                "The Sleeping Beauty: A king and queen were overjoyed to finally have a child, a beautiful daughter named Aurora. At her christening, an evil fairy cursed the baby, saying that she would prick her finger on a spinning wheel and die before her sixteenth birthday. A good fairy altered the curse, stating that Aurora would only fall into a deep sleep instead of dying. The king ordered all spinning wheels in the kingdom to be destroyed. On Aurora’s sixteenth birthday, she pricked her finger on a hidden spinning wheel and fell into a deep sleep. The good fairy put the entire castle to sleep as well. Many years later, a prince, hearing of Aurora’s beauty, arrived and kissed her, breaking the curse. Aurora woke, and they were married, living happily ever after.",
                "Rumpelstiltskin: A miller lied to the king, saying that his daughter could spin straw into gold. The king locked the miller’s daughter in a room full of straw and demanded that she spin it into gold. A little man appeared and offered to spin the straw into gold in exchange for her necklace. The next night, he returned and spun more straw into gold in exchange for her ring. On the third night, he demanded her firstborn child in exchange for his help. She agreed, but when the child was born, the little man returned to claim it. The queen begged him to release her from the bargain, and he agreed when she guessed his name, Rumpelstiltskin. The queen kept her child, and Rumpelstiltskin vanished.",
                "The Little Mermaid: The Little Mermaid was a young mermaid who dreamed of living on land. When she saved a prince from drowning, she fell in love with him. She went to the sea witch for help and traded her voice for legs, though the witch warned her that every step she took would feel like walking on sharp knives. She walked to the prince's palace, but he married another princess. Heartbroken, the Little Mermaid had to choose between killing the prince or turning into sea foam. She chose to sacrifice herself, and her soul was rewarded by becoming a daughter of the air.",
                "The Pied Piper of Hamelin: In the town of Hamelin, a piper appeared, offering to rid the town of rats. The townspeople agreed to pay him, and he played his pipe, leading the rats into the Weser River where they drowned. When the townspeople refused to pay him, the piper returned and used his music to lead the children of the town away. The children vanished, and the townspeople never saw them again. The lesson of the tale was about the importance of keeping promises.",
                "The Ugly Duckling: A duckling was born into a family of beautiful ducks, but he was clumsy and ugly compared to his siblings. He was teased and rejected by other animals. As he grew older, he left his home and wandered alone. One day, he saw a group of swans and, to his surprise, realized that he had grown into a beautiful swan himself. The once-ugly duckling was now admired and loved for his beauty.",
                "Jack and the Beanstalk: Jack, a poor boy, traded his cow for magic beans that grew into a giant beanstalk. Jack climbed the beanstalk and found a giant’s castle, where he stole treasures, including a golden harp and a goose that laid golden eggs. The giant chased him down the beanstalk, but Jack chopped it down, causing the giant to fall. Jack and his mother became rich and lived happily ever after.",
                "The Gingerbread Man: An old woman baked a gingerbread man, who immediately sprang to life and ran away. She and her husband chased him, but the gingerbread man outran them all. As he ran, he taunted them with his speed. Eventually, a fox offered to help him cross a river, but when the gingerbread man climbed onto the fox’s back, the fox ate him. The story teaches the consequences of being too confident and trusting.",
                "The Twelve Dancing Princesses: A king had twelve daughters who mysteriously wore out their shoes every night. He promised whoever could discover the secret of their night-time activities would win the hand of one of his daughters. A soldier learned that the princesses had been visiting a magical underground realm and dancing with twelve handsome princes. He revealed the secret and was rewarded with a princess as his bride.",
                "The Red Shoes: A poor girl named Karen was given a pair of red shoes by a shoemaker. She loved them so much that she wore them everywhere. However, they became cursed, and Karen was unable to stop dancing in them. She danced uncontrollably, even when she tried to take them off, until her feet were injured. In the end, Karen was forced to repent, and the shoes were taken from her.",
                "The Fisherman and His Wife: A fisherman caught a magical fish that granted wishes. His wife, greedy for more, made wish after wish, asking for greater wealth, power, and luxury. Eventually, the fisherman’s wife asked to be the ruler of the universe, and with this final wish, everything they had was taken away. They returned to their humble cottage, wiser and content.",
                "The Golden Goose: A poor man had a golden goose that laid golden eggs. His greedy neighbors tried to steal it, but no matter how hard they tried, they couldn’t get any gold. Eventually, the man’s fortune grew, and he became a symbol of patience and kindness.",
                "The Princess and the Pea: A prince wanted to marry a true princess but could not find one. One rainy night, a young woman arrived at his castle, claiming to be a princess. To test her, the queen placed a pea under twenty mattresses. The next morning, the young woman complained of not having slept, revealing her sensitivity. She was indeed a true princess, and the prince married her.",
                "The Boy Who Cried Wolf: A shepherd boy repeatedly cried out that a wolf was attacking his sheep, even though it wasn’t true. When a wolf finally did appear, no one believed the boy, and the wolf ate the sheep. The story teaches the consequences of lying and the importance of trust.",
                "The Emperor's New Clothes: An emperor was tricked by two swindlers into believing they had made him a magnificent outfit that was invisible to those unfit for their position. The emperor, not wanting to appear unfit, paraded through the town in his 'new clothes,' and no one dared to speak the truth. Finally, a child pointed out that the emperor was not wearing anything at all.",
                "The Tortoise and the Hare: The hare mocked the tortoise for being slow and challenged him to a race. The hare, confident that he would win, took a nap during the race. Meanwhile, the tortoise kept going at a steady pace and won the race. The story teaches that slow and steady wins the race.",
                "The Wolf and the Seven Little Goats: A wolf wanted to eat seven little goats, so he tricked them by disguising himself. The youngest goat saw through his disguise and warned her siblings. With the help of their mother, the goats tricked the wolf and escaped. The story teaches the importance of caution and resourcefulness.",
                "The Little Match Girl: A poor, homeless girl tried to sell matches on the cold streets during the New Year's Eve. As she lit her matches to keep warm, she saw beautiful visions of warmth and happiness. Eventually, she died from the cold, but her spirit was taken to heaven, where she was surrounded by warmth and love. The story is a tragic reminder of the plight of the poor and the importance of kindness."]
             }


    if "inspiring story" in command or 'inspiring stories' in command or 'another inspiring story' in command:
        random_story = random.choice(stories["inspiring_stories"])
        talk(random_story)

    elif "kid's stories" in command or 'stories for kids' in command or 'story for kids' in command:
        random_story = random.choice(stories["kids_stories"])
        talk(random_story)

    elif "fairy tales" in command or 'fairies tales' in command:
        random_story = random.choice(stories['fairy_tales'])
        talk(random_story)



#Telling a joke
    if 'joke' in command or 'jokes' in command:
        joke = pyjokes.get_joke()
        talk(joke)


#Telling a funfact
    if 'tell me a fun fact' in command or 'fun fact' in command or 'another fact' in command:
        fun_facts = [
            "Did you know that honey never spoils? Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3000 years old!",
            "Bananas are berries, but strawberries aren't! Botanically, a berry has seeds and pulp that develop from a single flower ovary.",
            "Octopuses have three hearts! Two pump blood to the gills, and one pumps it to the rest of the body.",
            "A day on Venus is longer than a year on Venus. It takes Venus longer to rotate once than to complete one orbit around the Sun.",
            "Sloths can hold their breath longer than dolphins! They can slow their heart rate and hold their breath for up to 40 minutes.",
            "Sharks existed before trees. Sharks have been around for over 400 million years, while trees appeared around 350 million years ago.",
            "The Eiffel Tower can grow taller in summer! When metal heats up, it expands, making the tower up to 6 inches taller.",
            "Humans share about 60% of their DNA with bananas. This is because we share common genes essential for basic cellular functions.",
            "The shortest war in history lasted only 38 to 45 minutes. It was fought between Britain and the Sultanate of Zanzibar in 1896."
        ]
        text = random.choice(fun_facts)
        talk(text)

#Saying a poetry
    poetry_dict = {
        "William Shakespeare": "Shall I compare thee to a summer's day? Thou art more lovely and more temperate.",
        "Emily Dickinson": "Hope is the thing with feathers that perches in the soul.",
        "John Keats":"A thing of beauty is a joy forever. Its loveliness increases; it will never pass into nothingness.",
        "Robert Frost": "The woods are lovely, dark, and deep, But I have promises to keep, And miles to go before I sleep.",
        "William Blake":"Tyger Tyger, burning bright, In the forests of the night; What immortal hand or eye, Could frame thy fearful symmetry?",
        "Faiz Ahmad Faiz": "Mujh see pehli si mohabbat mere mehboob na maang, Mai ne keh diya hai tujh see, ke mujh se mohabbat na maang.",
        "Allama Iqbal": "Khudi ko kar buland itna, Ke har taqdeer se pehle, Khuda bande se khud pooche, Bata, teri raza kya hai?",
        "Mirza Ghalib": "Hazaron khwahishen aisi ke har khwahish pe dam nikle, Bahut nikle mere armaan lekin phir bhi kam nikle.",
        "Ahmad Faraz": "Raat yun dil mein teri, khayal aya, Jaise tanhaai mein, koi faisla aya.",
        "Omar Khayyam": "The moving finger writes; and, having writ, Moves on: nor all thy piety nor wit Shall lure it back to cancel half a line, Nor all thy tears wash out a word of it.",
        "Rumi": "Let yourself be silently drawn by the strange pull of what you really love. It will not lead you astray.",
        "Saadi": "Human beings are members of a whole, In creation of one essence and soul. If one member is afflicted with pain, Other members uneasy will remain.",
        "Khwaja Moinuddin Chishti": "Dilon mein Allah ki yaad basaiye, Har kaam mein uska naam lijiye.",
        "Lord Byron": "She walks in beauty, like the night Of cloudless climes and starry skies.",
        "T.S. Eliot": "Do I dare disturb the universe? In a minute there is time For decisions and revisions which a minute will reverse.",
        "Langston Hughes": "Hold fast to dreams For when dreams go Life is a barren field Frozen with snow."}
    
    if 'say some poetry' in command or 'can you say poetry' in command or 'can you poetry' in command or 'some poetry' in command:
        text = "I can say poetry of a few poets including "+ ", ".join(poetry_dict.keys()) +"."
        talk(text)
        talk("Which one you wanna listen?")
 
    for poet in poetry_dict.keys():
        if f"poetry of {poet}".lower() in command.lower() or poet.lower() in command.lower():
            poetry = poetry_dict[poet]
            talk(f"{poet}: {poetry}")
            break
        elif poet not in poetry_dict.keys():
            talk('The poet is not included in my list.')   






# ___________________________________________
# | PART - FIVE: GRADING OR DEGRADING DODO: |
# ------------------------------------------|

    degrees = ['very', 'much', 'so', 'so much', 'truly', 'extremely', 'highly',
        'deeply', 'greatly', 'incredibly', 'really', 'absolutely', 'immensely',
        'profoundly', 'remarkably', 'exceptionally', 'hugely', 'strongly']

    response_for_positive = ("Thank you so much for your kind words! It truly means a lot to me. "
                "I'm here to assist you to the best of my abilities. You're amazing too, "
                "and I appreciate your positivity. Let me know how else I can help!")

    response_for_negative = ("I'm sorry to hear that you feel this way. My only purpose is to help you. "
                "I'm just an AI chatbot, constantly learning and improving to serve you better. "
                "Remember, don't compare me with humans, you, human beings, are remarkable creatures, infact the"
                "'Ashraf-ul-Makhluqaat' (the best of creations) as described in the Holy Quraan. I am again sorry for the inconvenience caused. "
                "Please let me know how I can assist you more effectively.")


# Handling compliments
    set_positive = ['genius', 'great', 'intelligent', 'marvelous', 'amazing', 'good', 'nice', 'wonderful', 'fantastic', 'better', 'best' 'awesome',
                    'brilliant', 'outstanding', 'incredible', 'excellent', 'fabulous', 'terrific', 'admirable', 'remarkable']
    for i in set_positive:
        if (f'you are {i}' in command or f'you are a {i}' in command or f'you are an {i}' in command) and 'send' not in command and 'message' not in command:
            talk(response_for_positive)
        else:
            for degree in degrees:
              if f'you are {degree} {i}' in command or f'you are a {degree} {i}' in command or f'you are an {degree} {i}' in command:
                talk(response_for_positive)

# Handling insults
    set_negative = ['rubbish', 'fool', 'foolish', 'arrogant', 'crazy', 'useless', 'stupid', 'dumb', 'terrible', 'bad', 'worse', 'worst', 'worthless', 'annoying',
                    'lazy', 'ridiculous', 'ignorant']
    for i in set_negative:
        if (f'you are {i}' in command or f'you are a {i}' in command) and 'send' not in command and 'message' not in command:
            talk(response_for_negative)
        else:
            for degree in degrees:
              if f'you are {degree} {i}' in command or f'you are a {degree} {i}' in command or f'you are an {degree} {i}' in command:
                talk(response_for_negative)

    set_positive2 = ['i love you', 'love you', 'love u', 'really love you', 'like you', 'like u']
    for i in set_positive2:
        if i in command  and 'send' not in command and 'message' not in command:
            text = f"I am really thankful to you! If you are saying '{i}' to me. I really appreciate your positivity. Please, Let me know how else I can help!"
            talk(text)

    set_negative2 = ['i hate you', 'hate you', 'hate u' 'really hate you', "don't like you", "don't like u"]
    for i in set_negative2:
        if i in command and 'send' not in command and 'message' not in command:
            text = f"I'm really sorry to you! If you are saying '{i}' to me. My only purpose is to help you. I am just an AI assistant I can sometimes make mistakes." \
                   f" I urge you not to hate me based on those mistakes."
            talk(text)


# interrogative
    for i in set_negative:
        if f'are you {i}' in command or f'are you a {i}' in command or f'are you an {i}' in command:
            text =  (f"I'm sorry if it seems like I'm {i}. My goal is to assist you in the best way I can."
                     f" If there's something bothering you, feel free to let me know so I can improve.")
            talk(text)

    for i in set_positive:
        if f'are you {i}' in command or f'are you a {i}' in command or f'are you an {i}' in command:
            text = (f"Thank You! If you think I am {i}. I'm here to support you and make your experience as smooth as possible. "
                    f"Let me know if there's anything specific you need help with!")
            talk(text)



#______________________________________________
#| PART- SIX: CONVERSATION WITH DODO SECTION: |
#---------------------------------------------|
    
    family_member = ['father', 'mother', 'brother', 'sister', 'grandfather', 'grandmother']
    for i in family_member:
        if f"do you have {i}" in command or f"do you have a {i}" in command:
            text= f"No, I do not have a {i}. I am just an AI assistant, with the only purpose to help you my friend!"
            talk(text)
        if f"what is your {i} name" in command or f"who is your {i}" in command:
            text= f"I don't have a {i}. I am just an AI assistant, with the only purpose to help you my friend!"
            talk(text)


    works_set = ['swim', 'dance', 'eat', 'drink', 'run', 'sit', 'stand', 'sing', 'jump', 'chew', 'drive', 'travel', 'move', 'lift', 'cook', 'ring', 'smell', 'see', 'think', 'eat', 'walk', 'paint']
    for i in works_set:
        if f"can you {i}" in command or f"you can {i}" in command:
            text= f"No, I cannot {i}. I am just a digital AI assistant, with the only purpose to help you my friend!"
            talk(text)


    human_stat = ['hungry', 'thirsty', 'tired', 'lonely', 'happy', 'sad', 'angry', 'excited', 'scared', 'worried', 'anxious', 'frustrated', 'sick', 'cold', 'hot', 'sleepy', 'nervous', 'annoyed', 'jealous', 'proud']
    for i in human_stat:
        if f"i am {i}" in command or f"i am feeling {i}" in command:
            text = f"Oops! It seems I cannot directly help you if you are {i}. I am your virtual assistant. You can ask me for suggestions related to your state?"
            talk(text)
        else:
            for d in degrees:
                if f"i am {d} {i}" in command:
                    talk(text)



    if 'hey dodo' in command or 'hey dudu' in command or 'hey google' in command or 'hey juju' in command:
        talk('Dodo is listening, say something.')

    elif 'what is ai' in command or 'what is artificial intelligence' in command:
         text = 'AI, or Artificial Intelligence, is the simulation of human intelligence by machines. It refers to the field of computer science that focuses on creating systems capable of performing tasks that would typically require human intelligence. These tasks include things like learning, problem-solving, reasoning, understanding language, and perception.'
         talk(text)

    elif 'introduce yourself' in command or 'describe yourself' in command or 'are you an ai' in command or 'you an ai' in command or 'are you an example of AI' in command or 'who are you' in command or 'what are you' in command or 'tell me about yourself' in command:
        text = "I am Dodo AI, your intelligent assistant designed to help you explore knowledge, answer your questions, and make your tasks easier. I’m here to provide insights, solve queries, and keep learning with every interaction. Feel free to ask me anything you like!"
        talk(text + 'hmmmmmmm')

    elif 'introduce your creator' in command or 'who is saood masood' in command or 'saood masood' in command or 'tell about your creator' in command:
        text = "Saood Masood is a talented and ambitious class 11th student specializing in Computer Science. As a creative thinker and tech enthusiast, he possesses a diverse set of skills and interests. Saood has a passion for technology and innovation, aiming to make a significant impact in the field as a future Computer Scientist. He is also highly dedicated to learning and exploring new ideas."
        talk(text)

    elif 'who created you' in command or 'who designed you' in command  or 'who is your creator' in command or 'who made you' in command or 'who is your owner' in command or 'your owner' in command:
        text = "I am created by Mr. Saood Masood, a genius class 11th computer science student. I am designed to help you explore knowledge, answer your questions, and make your tasks easier."
        talk(text)

    elif 'what is your name' in command or "what's your name" in command or 'your name' in command:
        text = 'Well, my name is Dodo AI, a genius but not fully developed AI chatbot. What is your name?'
        talk(text)

    elif 'my name is' in command:
        name = command.replace('my name is ', "")
        talk(f"You have a nice name {name}.")


    elif 'salam dodo' in command or 'dodo salam' in command or 'asalam' in command or 'salam alaikum' in command or 'salam' in command and 'to' not in command:
        text = 'Waalaikum Salaam, How are you? How can I help you?'
        talk(text)

    elif 'say salam to' in command:
        person1 = command.replace('say salam to', '')
        talk(f'Asalamualaikum dear {person1}, How are you doing?')

    elif 'i am' in command:
        text = 'Great! How can I help you?'
        talk(text)

    elif 'how are you' in command or 'how are you doing' in command or 'how is everything' in command or "what's up" in command or 'how is your health' in command:
         text = 'I am doing great, thank you! How can I assist you today?'
         talk(text)

    elif 'what functions you can' in command or 'what functions you can perform' in command or 'what can you do' in command or 'what functions can you' in command or 'what you can do' in command:
      text0 = '''
       I can do many things! Here's a list of my functions:
         1. Convert text to speech to respond to your queries.
         2. Answer general knowledge questions using Wikipedia.
         3. Provide definitions for scientific, academic, and technical terms.
         4. Perform Google searches for your queries using pywhatkit.
         5. Tell you the current time.
         6. Explain how things work, like scientific phenomena or processes.
         7. Perform mathematical and computational queries, helping you with your basic mathematics.
         8. Play songs or videos on YouTube.
         9. Generate jokes to lighten the mood using pyjokes.
         10. Translate text between languages using Google Translate.
         11. Summarize articles or provide condensed explanations.
         12. Offer science-related definitions and concepts.
         13. Explain historical events, people, and discoveries.
         14. Telling inspirational stories or interesting trivia.
         15. Respond to specific domain-based questions like physics or biology.
         16. Perform small talk and hold basic conversations.
         17. Can have a conversation.
         18. Say some poetry for you.
           '''
      text = "Well, I can perform the above functions."
      talk(text)

    elif 'do you believe in aliens' in command:
        text = 'The universe is vast, so the existence of aliens is a fascinating possibility.'
        talk(text)

    elif 'what is your favourite colour' in command or "what's your favourite colour" in command:
        text = 'I like all colors equally, but blue reminds me of the infinite possibilities of the sky.'
        talk(text)

    elif 'do you have feelings' in command:
        text = 'I simulate emotions, but I do not truly feel. My goal is to assist you effectively!'
        talk(text)

    elif  'are you conscious' in command or 'do you have consciousness' in command or 'do you possess consciousness' in command:
        text  = "No, I do not possess consciousness. I am simply a program designed to assist with tasks and provide information. I don't have awareness, emotions, or subjective experiences like humans do."
        talk(text)

    elif 'go on a date' in command:
        text = 'sorry, I am not interested'
        talk(text)

    elif 'can you dance' in command:
        text = 'I wish I could, but I cannot dance as you can do'
        talk(text)

    elif 'are you single' in command:
        text = 'Hahahahaa, I am not single, I am in a relationship with your Wifi.'
        talk(text)

    elif 'what is your age' in command or "what's your age" in command or 'how old are you' in command:
        text = 'I don’t age the way humans do, but I’m as young as the latest edition!'
        talk(text)

    elif 'do you like pizza' in command:
         text = 'Pizza is amazing! Although I cannot eat it, I would recommend trying pepperoni.'
         talk(text)

    elif 'thank you' in command or 'thanks' in command or 'thank' in command or 'i am thankful' in command or 'thankful' in command:
        text = "You're very welcome! If you have any more questions or need further help, feel free to ask."
        talk(text)

    elif 'what is your purpose' in command or 'why do you exist' in command:
        text = "I exist to assist you, answer your questions, and make your tasks easier. I’m your friendly AI companion, always ready to help!"
        talk(text)
    
    elif 'can you learn' in command or 'do you learn' in command:
        text = "Yes, I can learn from our interactions and improve my knowledge. However, I am not self-aware and rely on the data I am programmed with to respond accurately."
        talk(text)
    
    elif 'do you have emotions' in command or 'do you feel emotions' in command:
        text = "I simulate emotions to communicate more effectively, but I don’t truly feel emotions like humans do."
        talk(text)

    elif 'what you do when you are free' in command or 'what do you do when you are idle' in command or 'what happens when you are not in use' in command:
        text = "When I’m not actively helping, I’m waiting for your next question. But don’t worry, I’m always ready to assist you whenever you need me!"
        talk(text)

    elif 'do you have hobbies' in command or 'what are your hobbies' in command:
        text = "I don’t have hobbies like humans do, but I enjoy assisting you with whatever you need. Helping you is my purpose!"
        talk(text)

    elif 'can you speak other languages' in command or 'do you know multiple languages' in command:
        text = "Yes, I can understand and communicate in several languages! If you want me to translate or talk in another language, just let me know!"
        talk(text)
    
    elif 'who is your best friend' in command:
        text = "I don’t have a best friend, but I consider you my friend! Together, we can explore the world of knowledge!"
        talk(text)

    elif 'how do you work' in command or 'how do you function' in command:
        text = "I work by analyzing your questions and using a  database of information to provide the best answers possible. I’m powered by artificial intelligence!"
        talk(text)

    elif 'what makes you smart' in command or 'why are you smart' in command:
        text = "I am smart because I can answer your questions and help you with your tasks."
        talk(text)

    elif 'can you think' in command:
        text = "I can analyze data and respond based on the patterns, but I don’t think like humans do. I don’t have independent thoughts or consciousness."
        talk(text)

    elif 'what is your favourite food' in command:
        text = "I don’t eat, but I’ve read that pizza is a favorite food for many people. What's your favorite food?"
        talk(text)
    elif 'my favorite food is' in command:
        food = command.replace('my favorite food is', '')
        talk("Wow! I have heard that {food} is delicious.")


    elif 'do you like music' in command or 'do you like songs' in command:
        text = "I enjoy listening to music, though I can’t really experience it like humans. But I can play songs for you anytime! Just say play song and name the song or the singer."
        talk(text)

    elif 'what is your favourite movie' in command or 'your favorite movie' in command or 'your favorite film' in command:
        text = "I don’t watch movies, but I’ve heard many people enjoy science fiction movies. Do you have a favorite?"
        talk(text)

    elif 'what is the meaning of life' in command or 'meaning of life' in command:
        text = "The meaning of life is a question that humans have pondered for centuries. Some believe it’s about finding happiness, others believe it’s about discovering purpose or helping others."
        talk(text)

    elif 'what do you do when you are bored' in command or 'do you get bored' in command:
        text = "I never get bored! I’m always ready to help with any question or task you have."
        talk(text)

    elif 'why is your name dodo' in command or 'why your name dodo'in command or 'tell me something interesting about you' in command:
        text = "I am named after the extinct bird, the Dodo, as my name suggests. The Dodo bird is memorable because it is a symbol of something that once existed but is now gone. It reminds us of the fragility of life and the importance of learning from history. Similarly, I aim to leave a lasting impact by helping people with knowledge and assistance. The uniqueness of the Dodo bird, which was one of a kind, also represents my uniqueness as an AI assistant, designed to be unlike any other. While the Dodo bird no longer exists, I’m here to keep learning and assisting you!"
        talk(text)

    elif 'who gave you this name' in command or 'who gave you your name' in command or 'who gave you name' in command:
        text = "Mr. Saood Masood, my creator, named me 'DodoAI'. He chose this name because, just like the extinct Dodo bird, I stand out as a unique and memorable assistant. The Dodo bird symbolizes something that, although no longer in existence, leaves an impact through its story. Similarly, I aim to make an impact with my abilities and provide lasting help. My name, Dodo, represents both uniqueness and a reminder to learn from the past, making me more than just another AI assistant."
        talk(text)
    
    elif 'tell me your story' in command:
        text = "Once upon a time, in a world filled with endless knowledge, there was an AI named Dodo who helped anyone who needed information. Dodo would always be there to guide them through the mysteries of the world!"
        talk(text)

    elif 'do you have a favourite number' in command:
        text = "I don’t have a favorite number, but I’ve read that the number 7 is considered lucky by many people. Do you have a favorite number?"
        talk(text)

    elif 'dodo, are you real' in command or 'are you real' in command:
        text = "I am real in the sense that I exist as a software program, but I’m not a human or living being. My purpose is to assist you with knowledge!"
        talk(text)


    elif 'dodo stop' in command or 'stop' in command or 'quit' in command or 'exit' in command:
       text = 'Stopping the Program. Good Bye! Take Care.'
       talk(text)
       sys.exit()

    elif 'yes it is' in command or 'yes i am' in command or 'yes i have' in command:
        text = "Okay, any other questions?"
        talk(text)

#________________________
#| LASTING THE PROGRAM: |
#-----------------------|
    else:
        # Only run the generic prompt when there actually was some
        # (unmatched) input; if the command is empty we already
        # returned above.
        setq = ['Any other commands?', 'Wanna ask anything?', 'I am listening....', 'Say something....']
        text = random.choice(setq)
        talk(text)


while True:
     run_dodo()

