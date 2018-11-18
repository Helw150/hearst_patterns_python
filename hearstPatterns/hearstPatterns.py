import re
import string
import spacy

class HearstPatterns(object):

    def __init__(self, extended = False):
        self.__adj_stopwords = ["a", "able", "about", "above", "abst", "accordance", "according", "accordingly", "across", "act", "actually", "added", "adj", "affected", "affecting", "affects", "after", "afterwards", "again", "against", "ah", "all", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "apparently", "approximately", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "auth", "available", "away", "awfully", "b", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "between", "beyond", "biol", "both", "brief", "briefly", "but", "by", "c", "ca", "came", "can", "cannot", "can't", "cause", "causes", "certain", "certainly", "co", "com", "come", "comes", "contain", "containing", "contains", "could", "couldnt", "d", "date", "did", "didn't", "different", "do", "does", "doesn't", "doing", "done", "don't", "down", "downwards", "due", "during", "e", "each", "ed", "edu", "effect", "eg", "eight", "eighty", "either", "else", "elsewhere", "end", "ending", "enough", "especially", "et", "et-al", "etc", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "except", "f", "far", "few", "ff", "fifth", "first", "five", "fix", "followed", "following", "follows", "for", "former", "formerly", "forth", "found", "four", "from", "further", "furthermore", "g", "gave", "get", "gets", "getting", "give", "given", "gives", "giving", "go", "goes", "gone", "got", "gotten", "h", "had", "happens", "hardly", "has", "hasn't", "have", "haven't", "having", "he", "hed", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hers", "herself", "hes", "hi", "hid", "him", "himself", "his", "hither", "home", "how", "howbeit", "however", "hundred", "i", "id", "ie", "if", "i'll", "im", "immediate", "immediately", "importance", "important", "in", "inc", "indeed", "index", "information", "instead", "into", "invention", "inward", "is", "isn't", "it", "itd", "it'll", "its", "itself", "i've", "j", "just", "k", "keep", "        keeps", "kept", "kg", "km", "know", "known", "knows", "l", "largely", "last", "lately", "later", "latter", "latterly", "least", "less", "lest", "let", "lets", "like", "liked", "likely", "line", "little", "'ll", "look", "looking", "looks", "ltd", "m", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "million", "miss", "ml", "more", "moreover", "most", "mostly", "mr", "mrs", "much", "mug", "must", "my", "myself", "n", "na", "name", "namely", "nay", "nd", "near", "nearly", "necessarily", "necessary", "need", "needs", "neither", "never", "nevertheless", "new", "next", "nine", "ninety", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "now", "nowhere", "o", "obtain", "obtained", "obviously", "of", "off", "often", "oh", "ok", "okay", "old", "omitted", "on", "once", "one", "ones", "only", "onto", "or", "ord", "other", "others", "otherwise", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "owing", "own", "p", "page", "pages", "part", "particular", "particularly", "past", "per", "perhaps", "placed", "please", "plus", "poorly", "possible", "possibly", "potentially", "pp", "predominantly", "present", "previously", "primarily", "probably", "promptly", "proud", "provides", "put", "q", "que", "quickly", "quite", "qv", "r", "ran", "rather", "rd", "re", "readily", "really", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "respectively", "resulted", "resulting", "results", "right", "run", "s", "said", "same", "saw", "say", "saying", "says", "sec", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sent", "seven", "several", "shall", "she", "shed", "she'll", "shes", "should", "shouldn't", "show", "showed", "shown", "showns", "shows", "significant", "significantly", "similar", "similarly", "since", "six", "slightly", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "specifically", "specified", "specify", "specifying", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "        t", "take", "taken", "taking", "tell", "tends", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'll", "theyre", "they've", "think", "this", "those", "thou", "though", "thoughh", "thousand", "throug", "through", "throughout", "thru", "thus", "til", "tip", "to", "together", "too", "took", "toward", "towards", "tried", "tries", "truly", "try", "trying", "ts", "twice", "two", "u", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "up", "upon", "ups", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "v", "value", "various", "'ve", "very", "via", "viz", "vol", "vols", "vs", "w", "want", "wants", "was", "wasnt", "way", "we", "wed", "welcome", "we'll", "went", "were", "werent", "we've", "what", "whatever", "what'll", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "whose", "why", "widely", "willing", "wish", "with", "within", "without", "wont", "words", "world", "would", "wouldnt", "www", "x", "y", "yes", "yet", "you", "youd", "you'll", "your", "youre", "yours", "yourself", "yourselves", "you've", "z", "zero"]

        # now define the Hearst patterns
        # format is <hearst-pattern>, <general-term>
        # so, what this means is that if you apply the first pattern, the firsr Noun Phrase (NP)
        # is the general one, and the rest are specific NPs
        self.__hearst_patterns = [
            ('(NP_\\w+ (, )?such as (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
            ('(such NP_\\w+ (, )?as (NP_\\w+ ?(, )?(and |or )?)+)', 'first'),
            ('((NP_\\w+ ?(, )?)+(and |or )?other NP_\\w+)', 'last'),
            ('(NP_\\w+ (, )?include (NP_\\w+ ?(, )?(and |or )?)+)', 'first'),
            ('(NP_\\w+ (, )?especially (NP_\\w+ ?(, )?(and |or )?)+)', 'first'),
        ]

        if extended:
            self.__hearst_patterns.extend([
                ('((NP_\\w+ ?(, )?)+(and |or )?any other NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?some other NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?be a NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?like (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('such (NP_\\w+ (, )?as (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?like other NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?one of the NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?one of these NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?one of those NP_\\w+)', 'last'),
                ('example of (NP_\\w+ (, )?be (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?be example of NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?for example (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?wich be call NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?which be name NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?mainly (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?mostly (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?notably (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?particularly (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?principally (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?in particular (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?except (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?other than (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?e.g. (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?i.e. (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?a kind of NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?kind of NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?form of NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?which look like NP_\\w+)', 'last'),
                ('((NP_\\w+ ?(, )?)+(and |or )?which sound like NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?which be similar to (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?example of this be (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?type (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )? NP_\\w+ type)', 'last'),
                ('(NP_\\w+ (, )?whether (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(compare (NP_\\w+ ?(, )?)+(and |or )?with NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )?compare to (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('(NP_\\w+ (, )?among -PRON- (NP_\\w+ ? (, )?(and |or )?)+)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?as NP_\\w+)', 'last'),
                ('(NP_\\w+ (, )? (NP_\\w+ ? (, )?(and |or )?)+ for instance)', 'first'),
                ('((NP_\\w+ ?(, )?)+(and |or )?sort of NP_\\w+)', 'last')
            ])

        self.__spacy_nlp = spacy.load('en')
        
    def chunk(self, rawtext):
        doc = self.__spacy_nlp(rawtext)
        chunks = []
        for sentence in doc.sents:
            sentence_text = sentence.lemma_
            for chunk in sentence.noun_chunks:
                chunk_arr = []
                for token in chunk:
                    # Ignore Punctuation and stopword adjectives (generally quantifiers of plurals)
                    if token.is_punct or token.lemma_ in self.__adj_stopwords:
                        continue
                    chunk_arr.append(token.lemma_)
                chunk_lemma = " ".join(chunk_arr)
                replacement_value = "NP_"+"_".join(chunk_arr)
                sentence_text = sentence_text.replace(chunk_lemma, replacement_value)
            chunks.append(sentence_text)
        return chunks

    """
        This is the main entry point for this code.
        It takes as input the rawtext to process and returns a list of tuples (specific-term, general-term)
        where each tuple represents a hypernym pair.

    """
    def find_hyponyms(self, rawtext):

        hyponyms = []
        np_tagged_sentences = self.chunk(rawtext)

        for sentence in np_tagged_sentences:
            # two or more NPs next to each other should be merged into a single NP, it's a chunk error

            for (hearst_pattern, parser) in self.__hearst_patterns:
                matches = re.search(hearst_pattern, sentence)
                if matches:
                    match_str = matches.group(0)

                    nps = [a for a in match_str.split() if a.startswith("NP_")]

                    if parser == "first":
                        general = nps[0]
                        specifics = nps[1:]
                    else:
                        general = nps[-1]
                        specifics = nps[:-1]
                        print(str(general))
                        print(str(nps))

                    for i in range(len(specifics)):
                        #print("%s, %s" % (specifics[i], general))
                        hyponyms.append((self.clean_hyponym_term(specifics[i]), self.clean_hyponym_term(general)))

        return hyponyms


    def clean_hyponym_term(self, term):
        # good point to do the stemming or lemmatization
        return term.replace("NP_","").replace("_", " ")

