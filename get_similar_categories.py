from gensim.test.utils import datapath, get_tmpfile
from gensim.models import KeyedVectors

glove_file = datapath('/home/mathuryash5/7th Sem/Web Technologies - II/QuizUp/trained_model/glove.6B.50d.txt')
tmp_file = get_tmpfile("word2vec_50d.txt")
# calling glove2word2vec script
from gensim.scripts.glove2word2vec import glove2word2vec
glove2word2vec(glove_file, tmp_file)

model = KeyedVectors.load_word2vec_format(tmp_file)


res = model.most_similar("football", topn=10, restrict_vocab=None)

res = model.most_similar("science", topn=10, restrict_vocab=None)

res = model.most_similar("physics", topn=10, restrict_vocab=None)


print(res)