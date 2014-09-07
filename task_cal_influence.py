# -*- coding: utf-8 -*-

from underscore import _ as us
from pymongo import MongoClient, ASCENDING
import operator
from multiprocessing import Pool
import gc


gc.disable()

client = MongoClient()
db = client['github']
pageranks = db['pageranks']
influences = db['influences']


# def max_record(records):
#     return max(records, key=lambda x: x['pagerank'])


def cal_influence_ranking((actor, records)):
    # return (actor,
    #         sum(filter(lambda x: x > 1, us.pluck(
    #             map(max_record,
    #                 group_by(lambda x: x['repo'], records).values()),
    #             'pagerank'))))
    return (actor, sum(filter(lambda x: x > 1, us.pluck(records, 'pagerank'))))


def influence_ranks(spec):
    pool = Pool()
    ranks = sorted(
        pool.map(cal_influence_ranking, us.groupBy(
            list(pageranks.find(spec)), 'actor').items()),
        key=operator.itemgetter(1), reverse=True)

    pool.close()
    pool.join()

    return ranks


influence_specs = {
    'General': {},
    'JavaScript': {'language': 'JavaScript'},
    'CSS': {'language': 'CSS'},
    'Python': {'language': 'Python'},
    'Ruby': {'language': 'Ruby'},
    'Go': {'language': 'Go'},
    'PHP': {'language': 'PHP'},
    'Shell': {'language': 'Shell'},
    'Perl': {'language': 'Perl'},
    'Objective-C': {'language': 'Objective-C'},
    'Swift': {'language': 'Swift'},
    'Java': {'language': 'Java'},
    'C++': {'language': 'C++'},
    'C#': {'language': 'C#'},
    'C': {'language': 'C'},
    'Haskell': {'language': 'Haskell'},
    'Scala': {'language': 'Scala'},
    'Erlang': {'language': 'Erlang'},
    'Clojure': {'language': 'Clojure'}
}


def main():
    for field, spec in influence_specs.items():
        ranks = influences.find({'field': field})

        if not ranks:
            ranks = influence_ranks(spec)

            influences.insert({
                'field': field,
                'ranks': ranks
            })

        print '%s top 25:' % field
        for i, (actor, pagerank) in enumerate(ranks[:25]):
            print str(i + 1) + '.', actor, pagerank

        print '%s top 25(hide score):' % field
        for i, (actor, pagerank) in enumerate(ranks[:25]):
            print str(i + 1) + '.', actor


if __name__ == '__main__':
    main()
