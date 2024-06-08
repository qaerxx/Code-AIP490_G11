import spacy
import string

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

class FragmentDetection(object):

    def __init__(self, sentence):
       exclude = set(string.punctuation)
       self.sentence = ''.join(ch for ch in sentence if ch not in exclude)
       self.tags = nlp(self.sentence)

    def check_predicate(self):  # check if a sentence has a predicate or not
        predicate_se = True
        matches = []
        for i in range(len(self.tags)):
            index = 0
            if self.tags[i].pos_ == "VERB" or self.tags[i].pos_ == "AUX":
                index = i
            while index > 0 and index < len(self.tags):
                matches.append(self.tags[index])
                index += 1
            if index > 0:
                break
        if len(matches) <= 1:
            predicate_se = False
        return predicate_se
    
    def sconj_usage(self): #solve case using sconj. Ex: Because of tuition, he was worked in night. 
        sconj_usage = False
        for i in range(len(self.tags)): #take "Because of tuition" and put it to matches[], af
            index = -1
            if self.tags[i].pos_ == "SCONJ":
                index = i
            while index >= 0 and index < len(self.tags)-1:
                if(self.tags[index+1].dep_ in ("nsubj", "nsubjpass", "csubj", "csubjpass", "expl")):  
                    return sconj_usage
                if(self.tags[index+1].dep_ == "pobj"):
                    sconj_usage = True
                    return sconj_usage
            if index >= 0:
                break
        return sconj_usage

    def fragment_in_sentence(self):
        SUBJ = []
        fragment_se = False
        sconj = False
        if not self.check_predicate():
            fragment_se = True
            return fragment_se
        for token in self.tags:
            if token.pos_ == "SCONJ":
                sconj = True
        if sconj:
            for i in self.tags:
                if i.dep_ in ("nsubj", "nsubjpass", "csubj", "csubjpass", "expl"):
                    SUBJ.append(i)
            if len(SUBJ) <= 1:
                fragment_se = True
        else:
            for i in self.tags:
                if i.dep_ in ("nsubj", "nsubjpass", "csubj", "csubjpass", "expl"):
                    SUBJ.append(i)
            if len(SUBJ) == 0:
                fragment_se = True
        return fragment_se

def process_essay(essay):
    # Split essay into sentences
    doc = nlp(essay)
    sentences = [sent.text.strip() for sent in doc.sents]


    # Analyze each sentence
    results = {}
    for sentence in sentences:
        np_extractor = FragmentDetection(sentence)
        is_fragment = np_extractor.fragment_in_sentence()
        results[sentence] = is_fragment


    return results


# Input essay
essay = "Because we are student."

# Process the essay
results = process_essay(essay)

# Output the results
for sentence, is_fragment in results.items():
    if is_fragment:
        status = "Fragment" 
        print(f"'{sentence}': {status}")

