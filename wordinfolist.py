class WordInfoList:

    def __init__(self, data):
        entries = data.split('|')

        if len(entries) < 4:
            raise ValueError('At least list name, file, seperator and word index must be specified.')

        self.name = entries[0]
        self.path = entries[1]

        # Parse sperator
        self.seperator = entries[2]
        self.seperator = self.seperator.replace('\\t', '\t')
        if self.seperator == '':
            self.seperator = '\n'

        # Parse index entry
        index_entry = entries[3]

        if not index_entry.startswith('$'):
            raise ValueError('The word data index is not valid. Example: $1')

        try:
            self.index = int(index_entry[1:]) - 1
        except:
            raise ValueError('The word data index is not valid. Example: $1')
            
        if self.index < 0:
            raise ValueError('The word data index is not valid. Example: $1')
        
        # Parse fields
        self.fields = []

        for e in entries[4:]:
            f = e.split(':')
            if len(f) != 2:
                raise ValueError(F'The field "{e}" is not valid.')
            self.fields.append((f[0].strip(), f[1].strip()))

        # Lost list
        self.load()


    def load(self):
        self.words = {}

        try:
            f = open(self.path, 'r', encoding='utf-8-sig')
        except:
            raise ValueError('Opening list file failed.')

        i = 1
        for l in f:
            segs = l.rstrip().split(self.seperator)
            if len(segs) <= self.index:
                continue
            self.words[segs[self.index]] = [str(i)] + segs
            i += 1

        f.close()


    def field_names(self):
        return [name for (name,_) in self.fields]


    def field_data(self, word):
        data = self.words.get(word)

        if data is None:
            return ['-'] * len(self.fields)

        ret = []
        for (_,f) in self.fields:
            # ugly, but I'm lazy
            for i in range(len(data)):
                f = f.replace(F'${i}', data[i])
            ret.append(f)

        return ret
