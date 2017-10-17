# coding=utf-8
from __future__ import absolute_import

from mongokit import Document
from mongokit.document import DocumentProperties
from inflection import underscore, pluralize
import time


class MetaDoc(DocumentProperties):

    def __init__(cls, name, bases, attrs):
        super(MetaDoc, cls).__init__(name, bases, attrs)
        if not name.startswith('Callable'):
            if '__collection__' not in cls.__dict__:
                cls.__collection__ = pluralize(underscore(cls.__name__))
        return


class BaseDocument(Document):
    __metaclass__ = MetaDoc
    use_schemaless = False

    sensitive_fields = []

    def sensitive_filter(self, obj, repl='*'):
        if isinstance(obj, basestring):
            return dfa_filter.filter(obj, repl)
        elif isinstance(obj, dict):
            res = {}
            for k, v in obj.iteritems():
                res[k] = dfa_filter.filter(v, repl)
            return res
        elif isinstance(obj, list):
            res = []
            for item in obj:
                res.append(dfa_filter.filter(item, repl))
            return res
        else:
            return obj

    def _offset(self, offset):
        if not isinstance(offset, int):
            offset = 0
        return offset

    def _limit(self, limit, default=60):
        if not isinstance(limit, int):
            limit = 0
        if default and not limit:
            limit = default
        return min(limit, default)

    def save(self, *args, **kwargs):
        for key in self.sensitive_fields:
            self[key] = self.sensitive_filter(self[key])
        if 'updated' in self:
            self['updated'] = int(time.time())
        return super(BaseDocument, self).save(*args, **kwargs)

    def silent_save(self, *args, **kwargs):
        return super(BaseDocument, self).save(*args, **kwargs)


# filters
class DFAFilter():

    """Filter Messages from keywords
    Use DFA to keep algorithm perform constantly
    >>> f = DFAFilter()
    >>> f.add('sexy')
    >>> f.filter('hello sexy baby')
    hello **** baby
    """

    def __init__(self):
        self.keyword_chains = {}
        self.delimit = '\x00'

    def parse(self, path):
        with open(path) as f:
            for line in f:
                self.add(line.strip())

    def add(self, keyword):
        if not isinstance(keyword, unicode):
            keyword = keyword.decode('utf-8')
        chars = keyword.lower().strip()
        if not chars:
            return
        level = self.keyword_chains
        for i in xrange(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                for j in xrange(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: 0}
                break
        if i == len(chars) - 1:
            level[self.delimit] = 0

    def in_latin_word(self, message, start, step_ins):
        start_char = message[start]
        if 0x4e00 <= ord(start_char) < 0x9fa6:  # is chinese
            return False
        if start > 0 and \
           (ord(message[start - 1]) < 0x4e00 or
            ord(message[start - 1]) >= 0x9fa6) and \
           message[start - 1].isalnum():
            return True
        if start + step_ins < len(message) and \
           (ord(message[start + step_ins]) < 0x4e00 or
            ord(message[start + step_ins]) >= 0x9fa6) and \
           message[start + step_ins].isalnum():
            return True
        return False

    def filter(self, message, repl="*"):
        if not isinstance(message, str) and not isinstance(message, unicode):
            return message

        if isinstance(message, str):
            message = message.decode('utf-8')
        content_list = []
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        if self.in_latin_word(message, start, step_ins):
                            step_end = start + step_ins
                            content_list.append(message[start:step_end])
                            start += step_ins - 1
                            break
                        else:
                            content_list.append(repl * step_ins)
                            start += step_ins - 1
                            break
                else:
                    content_list.append(message[start])
                    break
            else:
                content_list.append(message[start])
            start += 1
        result = ''.join(content_list)
        return unicode(result)

    def check_legal(self, message, user_id):
        if not isinstance(message, unicode):
            message = message.decode('utf-8')
        message = message.lower()
        start = 0
        while start < len(message):
            level = self.keyword_chains
            step_ins = 0
            for char in message[start:]:
                if char in level:
                    step_ins += 1
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        return False
            start += 1
        return True

dfa_filter = DFAFilter()
dfa_filter.parse('badwords.txt')
