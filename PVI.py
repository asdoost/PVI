#!/usr/bin/env python3
from tabulate import tabulate

class PVI(object):
    """
    >>> verb = PVI('گذشت')
    >>> verb.inflect()
    -------  ------  --------  ----------  --------  -------------  ---------------  -----------
    می‌گذرم   گذشتم   گذشته‌ام   گذشته‌بودم   می‌گذشتم    دارم می‌گذرم    داشتم می‌گذشتم   خواهم گذشت
    می‌گذری   گذشتی   گذشته‌ای   گذشته‌بودی   می‌گذشتی    داری می‌گذری    داشتی می‌گذشتی   خواهی گذشت
    می‌گذرد    گذشت  گذشته‌است    گذشته‌بود    می‌گذشت    دارد می‌گذرد      داشت می‌گذشت   خواهد گذشت
    می‌گذریم  گذشتیم  گذشته‌ایم  گذشته‌بودیم  می‌گذشتیم  داریم می‌گذریم  داشتیم می‌گذشتیم  خواهیم گذشت
    می‌گذرید  گذشتید  گذشته‌اید  گذشته‌بودید  می‌گذشتید  دارید می‌گذرید  داشتید می‌گذشتید  خواهید گذشت
    می‌گذرند  گذشتند  گذشته‌اند  گذشته‌بودند  می‌گذشتند  دارند می‌گذرند  داشتند می‌گذشتند  خواهند گذشت
    -------  ------  --------  ----------  --------  -------------  ---------------  -----------
    """

    def __init__(self, word):
        file = open("data/irregulars.csv", 'r', encoding='utf-8')
        irregulars = map(lambda x: x.strip().split(','), file.readlines())
        lst = []
        for line in irregulars:
            if word in line:
                lst = [line[2], line[3], line[4]]
                break
        if not lst:
            if word.endswith('یدن'):
                self.infinitive = word
                self.present_stem = word[-3]
                self.past_stem = word[-2]
            elif word.endswith('ید'):
                self.infinitive = word + 'ن'
                self.present_stem = word[-2]
                self.past_stem = word
            else:
                self.infinitive = word + 'یدن'
                self.present_stem = word
                self.past_stem = word + 'ید'
        else:
            self.infinitive = lst[0]
            self.present_stem = lst[1]
            self.past_stem = lst[2]
        self.past_participle = self.past_stem + 'ه'

    def inflect(self):
        paradigm = {}
        paradigm['حال اخباری'] = ['می‌' + i for i in self.conjugation(self.present_stem, 'present')]
        paradigm['گذشته ساده'] = [i for i in self.conjugation(self.past_stem, 'past')]
        paradigm['حال کامل'] = [i for i in self.conjugation(self.past_participle, 'perfect')]
        paradigm['گذشته کامل'] = [self.past_participle + i for i in self.conjugation('‌بود', 'past')]
        paradigm['گذشته استمراری'] = ['می‌' + i for i in self.conjugation(self.past_stem, 'past')]
        paradigm['حال مستمر'] = [
        x + ' ' + y for x, y in zip(self.conjugation('دار', 'present'), paradigm['حال اخباری'])
        ]
        paradigm['گذشته مستمر'] = [
        x + ' ' + y for x, y in zip(self.conjugation('داشت', 'past'), paradigm['گذشته استمراری'])
        ]
        paradigm['آینده'] = [i + ' ' + self.past_stem for i in self.conjugation('خواه', 'present')]
        header = [
        'نوع تصریف',
        'اول شخص مفرد',
        'دوم شخص مفرد',
        'سوم شخص مفرد',
        'اول شخص جمع',
        'دوم شخص جمع',
        'سوم شخص جمع'
        ]

        table = tabulate(paradigm, stralign="right")
        print(table)
        return paradigm


    def conjugation(self, stem, tense):
        present = ['م', 'ی', 'د', 'یم', 'ید', 'ند']
        past = ['م', 'ی', '', 'یم', 'ید', 'ند']
        perfect = ['‌ام', '‌ای', '‌است', '‌ایم', '‌اید', '‌اند']

        if tense == 'present':
            return [stem + x for x in present]
        elif tense == 'past':
            return [stem + x for x in past]
        elif tense == 'perfect':
            return [stem + x for x in perfect]
        elif tense == 'future':
            return ['خواه' + x for x in present]
