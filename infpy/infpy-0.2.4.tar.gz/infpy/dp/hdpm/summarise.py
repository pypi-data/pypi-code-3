#
# Copyright John Reid 2008, 2009, 2010
#


"""
Summarise HDPM code.
"""


import logging, numpy, cookbook
from itertools import imap
from math import _greater_than
from cookbook import pylab_utils 
from cookbook.pylab_utils import pylab_ioff


def heatmap_categories(categories, category_names=None, distribution_names=None):
    "Plot the categories as a heat map."
    
    import pylab as P
    assert 2 == len(categories.shape)

    num_dists = categories.shape[0]
    assert None == distribution_names or len(distribution_names) == num_dists
    
    num_categories = categories.shape[1]
    assert None == category_names or len(category_names) == num_categories

    x_ind = numpy.arange(num_categories)
    y_ind = numpy.arange(num_dists)
    
    plt = P.pcolor(categories)
    P.colorbar()
    axes = P.gca()

    if None != category_names:
        axes.set_xticks(x_ind+.5)
        axes.set_xticklabels(category_names)
    else:
        axes.set_xticks(())
    for t in axes.xaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False

    if None != distribution_names:
        axes.set_yticks(y_ind+.5)
        axes.set_yticklabels(distribution_names)
    else:
        axes.set_yticks(())
    for t in axes.yaxis.get_major_ticks():
        t.tick1On = False
        t.tick2On = False

    
    


def plot_categories(categories, category_names=None, distribution_names=None, numrows=None, numcols=None):
    "Plot the categories as sub-plots."

    import pylab as P
    assert 2 == len(categories.shape)
    
    # determine number of rows and columns
    num_dists = categories.shape[0]
    num_categories = categories.shape[1]
    if not numrows and not numcols:
        numrows = int(numpy.sqrt(num_categories))
    if not numrows:
        numrows = num_categories / numcols
        if num_categories % numcols:
            numrows += 1
    elif not numcols:
        numcols = num_categories / numrows
        if num_categories % numrows:
            numcols += 1

    # plot each category        
    max, min = categories.max(), categories.min()
    ind = numpy.arange(num_dists)    # the x locations for the groups
    width = 1.                       # the width of the bars: can also be len(x) sequence
    for c in xrange(num_categories):
        splt = P.subplot(numrows, numcols, c+1)   # overlaps, subplot(111) is killed
        handles = [
            P.bar((i,), (x,), width, color=color)
            for color, i, x 
            in zip(pylab_utils.simple_colours, ind, categories[:,c])
        ]
        splt.set_ylim(min, max)
        if category_names:
            P.title(category_names[c])
        if c % numcols:
            splt.set_yticklabels(())
        if distribution_names:
            P.xticks(ind+width/2., distribution_names)
        else:
            splt.set_xticklabels(())
        splt.set_xticks(tuple())
    if distribution_names:
        P.figlegend(handles, distribution_names, 'upper right')
    

def _threshold_multinomial(x, threshold=.001):
    """
    @arg x: A discrete distribution.
    @return: Those indices that are greater than threshold/len(x)
    """
    return (x>=threshold/len(x)).nonzero()[0]





def threshold_dpm_based_on_posterior_enrichment_to_relative_most_enriched(
    dpm, num_topics_used,
    topic_word_threshold=5.,
    document_topic_threshold=5.
):
    """
    Thresholds the posterior of the DPM to associate topics with sets of words and documents.

    @return: (topic_word_match, document_topic_match) - 2 boolean arrays representing the associations
    """
    phi = dpm.exp_phi()[:num_topics_used]
    Phi = dpm.exp_Phi()
    phi_ratio = phi/Phi
    best_phis = phi_ratio.max(axis=1)
    topic_word_match = ((phi_ratio * topic_word_threshold).T > best_phis).T

    theta = dpm.exp_theta()[:,:num_topics_used]
    Theta = dpm.exp_Theta()[:num_topics_used]
    theta_ratio = theta/Theta
    best_thetas = theta_ratio.max(axis=1)
    document_topic_match = ((theta_ratio * document_topic_threshold).T > best_thetas).T

    return topic_word_match, document_topic_match



def threshold_dpm_based_on_posterior_enrichment(dpm, num_topics_used, topic_word_threshold=5., document_topic_threshold=5.):
    """
    Thresholds the posterior of the DPM to associate topics with sets of words and documents.

    @return: (topic_word_match, document_topic_match) - 2 boolean arrays representing the associations
    """
    phi = dpm.exp_phi()[:num_topics_used]
    Phi = dpm.exp_Phi()
    phi_ratio = phi/Phi
    topic_word_match = phi_ratio > topic_word_threshold

    theta = dpm.exp_theta()[:,:num_topics_used]
    Theta = dpm.exp_Theta()[:num_topics_used]
    theta_ratio = theta/Theta
    document_topic_match = theta_ratio > document_topic_threshold

    return topic_word_match, document_topic_match



def threshold_dpm_based_on_counts(dpm, num_topics_used, word_threshold=1., document_threshold=1.):
    """
    Thresholds the posterior of the DPM to associate topics with sets of words and documents.

    @return: (topic_word_match, document_topic_match) - 2 boolean arrays representing the associations
    """
    return dpm.counts.E_n_kw > word_threshold, dpm.counts.E_n_dk > document_threshold



class DpmStatistics(object):
    """
    Calculates statistics about the DPM.
    """

    def __init__(self, dpm):
        self.dpm = dpm
        self.update()

    def update(self, topic_size_threshold=1.):
        "Update the statistics."

        self.num_topics_used = (self.dpm.counts.E_n_k > topic_size_threshold).sum()
        """
        the number of topics that have an expected number of word counts greater than the topic_size_threshold
        """

        self.topic_word_match, self.document_topic_match = threshold_dpm_based_on_posterior_enrichment(self.dpm, self.num_topics_used)

        #self.topic_word_match, self.document_topic_match = threshold_dpm_based_on_counts(self.dpm, self.num_topics_used)

    def words_for_topic(self, k):
        "@return: The indices of those words that are likely to be drawn from topic k."
        return self.topic_word_match[k].nonzero()[0]

    def topics_for_word(self, w):
        "@return: The indices of those topics that have had word w drawn from them."
        return self.topic_word_match[:,w].nonzero()[0]

    def documents_for_topic(self, k):
        "@return: The indices of those documents that are expected to have drawn from topic k."
        return self.document_topic_match[:,k].nonzero()[0]

    def topics_for_document(self, d):
        "@return: The indices of those topics that are expected to have drawn from in document d."
        return self.document_topic_match[d].nonzero()[0]

    def num_topics_per_document(self):
        "@return: The number of topics per document."
        return [len(self.topics_for_document(d)) for d in xrange(self.dpm.D)]

    def num_documents_per_topic(self):
        "@return: The number of documents per topic."
        return [len(self.documents_for_topic(k)) for k in xrange(self.num_topics_used)]

    def num_words_per_topic(self):
        "@return: The number of words per topic."
        return [len(self.words_for_topic(k)) for k in xrange(self.num_topics_used)]

    def num_topics_per_word(self):
        "@return: The number of topics per word."
        return [len(self.topics_for_word(w)) for w in xrange(self.dpm.W)]

    def documents_for_top_topics(self, k):
        "@return: The documents associated with the topics above index k."
        documents = set()
        for k2 in xrange(k, self.num_topics_used):
            documents.update(self.documents_for_topic(k2))
        return documents

    def num_documents_by_top_topics(self):
        "@return: The number of documents associated with the top topics."
        return map(len, imap(self.documents_for_top_topics, xrange(self.num_topics_used)))




class DpmSummariser(object):
    """
    Summarises Dirichlet process mixtures.
    """

    def __init__(
      self,
      dpm,
      filename_prefix,
      document_ids=None,
      word_ids=None,
      document_tag='document',
      topic_tag='topic',
      word_tag='word',
      occurence_tag='occurence'
    ):
        """
        Constructs a DpmSummariser.

        @arg dpm: The Dirichlet process mixture.
        @arg filename_prefix: A prefix for the filenames the summariser generates.
        @arg document_ids: A list of identifiers for the documents.
        @arg word_ids: A list of identifiers for the words.
        @arg document_tag: A string to replace the word "document" with in the output.
        @arg topic_tag: A string to replace the word "topic" with in the output.
        @arg word_tag: A string to replace the word "word" with in the output.
        @arg occurence_tag: A string to replace the word "occurence" with in the output.
        """
        
        # decorate plotting functions to turn pylab interactive mode off
        self.pcolor = pylab_ioff(self.pcolor)
        self.imshow = pylab_ioff(self.imshow)
        self.plot_word_document_scatter = pylab_ioff(self.plot_word_document_scatter)
        self.plot_num_documents_by_top_topics = pylab_ioff(self.plot_num_documents_by_top_topics)
        self.make_topic_KL_heat_map = pylab_ioff(self.make_topic_KL_heat_map)
        self.topic_sizes = pylab_ioff(self.topic_sizes)
        self.topic_sizes_log_scale = pylab_ioff(self.topic_sizes_log_scale)
        self._histogram = pylab_ioff(self._histogram)
        self._plot_dist = pylab_ioff(self._plot_dist)
        self.make_topic_word_intersection_heat_map = pylab_ioff(self.make_topic_word_intersection_heat_map)
        self.make_topic_document_intersection_heat_map = pylab_ioff(self.make_topic_document_intersection_heat_map)
        self.make_phi_heat_map = pylab_ioff(self.make_phi_heat_map)
        self.make_theta_heat_map = pylab_ioff(self.make_theta_heat_map)
        
        if None == document_ids:
            document_ids = [str(i) for i in xrange(dpm.D)]
        if None == word_ids:
            word_ids = [str(i) for i in xrange(dpm.W)]

        self.dpm = dpm
        "The Dirichlet process mixture."

        self.statistics = DpmStatistics(dpm)
        "Statistics about the DPM."

        self.prefix = filename_prefix
        "A prefix for the filenames the summariser generates."

        self.document_ids = document_ids
        "A list of identifiers for the documents."

        self.word_ids = word_ids
        "A list of identifiers for the words."

        self.document_tag = document_tag
        'A string to replace the word "document" with in the output.'

        self.topic_tag = topic_tag
        'A string to replace the word "topic" with in the output.'

        self.word_tag = word_tag
        'A string to replace the word "word" with in the output.'

        self.occurence_tag = occurence_tag
        'A string to replace the word "occurence" with in the output.'


    def log_static_info(self):
        'Log information about the DPM that does not change.'
        logging.info('DPM data has %d %ss', self.dpm.D, self.document_tag)
        logging.info('DPM data has %d %ss', self.dpm.W, self.word_tag)
        logging.info('DPM is restricted to %d %ss', self.dpm.K, self.topic_tag)
        logging.info('DPM data has %d %ss', self.dpm.n_d.sum(), self.occurence_tag)


    def log_dynamic_info(self):
        'Log information about the DPM that does change.'

        self.statistics.update()

        logging.info('Using %d %ss', self.statistics.num_topics_used, self.topic_tag)

        logging.info(
          'Average number %ss per %s = %f',
          self.topic_tag,
          self.word_tag,
          numpy.mean(self.statistics.num_topics_per_word())
        )

        logging.info(
          'Average number %ss per %s = %f',
          self.word_tag,
          self.topic_tag,
          numpy.mean(self.statistics.num_words_per_topic())
        )

        logging.info(
          'Average number %ss per %s = %f',
          self.document_tag,
          self.topic_tag,
          numpy.mean(self.statistics.num_documents_per_topic())
        )

        logging.info(
          'Average number %ss per %s = %f',
          self.topic_tag,
          self.document_tag,
          numpy.mean(self.statistics.num_topics_per_document())
        )

        self.log_hyper_parameter_info()


    def save_fig(self, tag, **kwargs):
        from pylab import savefig
        savefig('%s-%s.eps' % (self.prefix, tag), format='EPS', **kwargs)
        #savefig('%s-%s.png' % (self.prefix, tag), format='PNG', **kwargs)

    def pcolor(self, Z, tag, size=1, **kwargs):
        import pylab as P
        P.figure()
        P.pcolor(Z)
        P.gca().set_xlim((0, Z.shape[0]))
        P.gca().set_ylim((0, Z.shape[1]))
        P.colorbar()
        self.save_fig(tag)
        P.close()

    def imshow(self, Z, tag, size=1, **kwargs):
        import pylab as P
        dpi = 100.
        figsize=numpy.array(Z.shape)/dpi
        #P.rcParams.update({'figure.figsize':figsize})
        fig = P.figure(figsize=figsize)
        P.axes([0,0,1,1]) # Make the plot occupy the whole canvas
        P.axis('off')
        fig.set_size_inches(size*figsize)
        P.imshow(Z, origin='lower', **kwargs)
        self.save_fig(tag, facecolor='black', edgecolor='black', dpi=dpi)
        P.close()

    def plot_word_document_scatter(self):
        "Make a scatter plot of number of words against number of documents for each topic."
        logging.info('Plotting word document scatter')
        import pylab as P
        P.figure()
        sizes = 3000.*self.dpm.counts.E_n_k/self.dpm.N
        P.scatter(
            self.statistics.num_words_per_topic(),
            self.statistics.num_documents_per_topic(),
            s=sizes
        )
        P.xlim(xmin=0)
        P.ylim(ymin=0)
        P.xlabel('\\# %ss' % self.word_tag)
        P.ylabel('\\# %ss' % self.document_tag)
        P.title('%ss vs. %ss vs. %ss' % (self.word_tag, self.document_tag, self.occurence_tag))
        self.save_fig('%s-%s-scatter' % (self.word_tag, self.document_tag))
        P.close()

    def plot_num_documents_by_top_topics(self):
        "Make a plot of number of documents depending on number of topics included."
        logging.info('Plotting number of documents')
        import pylab as P
        P.figure()
        P.plot(self.statistics.num_documents_by_top_topics())
        P.xlabel('%s cut-off' % self.topic_tag)
        P.ylabel('\\# %ss' % self.document_tag)
        #P.title('\\# %ss associated with top programs by size' % self.document_tag)
        self.save_fig('num-%ss-by-top-%ss' % (self.document_tag, self.topic_tag))
        P.close()

    def make_topic_KL_heat_map(self):
        "Make a heat map representing the distances between transcriptional programs."
        phi = self.dpm.exp_phi()
        K = self.statistics.num_topics_used
        Z = numpy.empty((K, K))
        for k1 in xrange(K):
            for k2 in xrange(K):
                Z[k1, k2] = discrete_KL(phi[k1], phi[k2])
        #self.imshow(Z, '%s-KL' % self.topic_tag, size=20, interpolation='nearest')
        self.pcolor(Z, '%s-KL' % self.topic_tag)
        return Z


    def make_topic_word_intersection_heat_map(self):
        "Make a heat map representing the distances between transcriptional programs."
        K = self.statistics.num_topics_used
        factors = [set(self.statistics.words_for_topic(k)) for k in xrange(K)]
        Z = numpy.zeros((K, K))
        for k1 in xrange(K):
            for k2 in xrange(K):
                if len(factors[k2]):
                    Z[k1, k2] = 1. - len(factors[k1].intersection(factors[k2])) / float(len(factors[k2]))
        #self.imshow(Z, '%s-%s-intersections' % (self.topic_tag, self.word_tag), size=20, interpolation='nearest')
        self.pcolor(Z, '%s-%s-intersections' % (self.topic_tag, self.word_tag))
        return Z


    def make_topic_document_intersection_heat_map(self):
        "Make a heat map representing the distances between transcriptional programs."
        K = self.statistics.num_topics_used
        documents = [set(self.statistics.documents_for_topic(k)) for k in xrange(K)]
        Z = numpy.zeros((K, K))
        for k1 in xrange(K):
            for k2 in xrange(K):
                if len(documents[k2]):
                    Z[k1, k2] = 1. - len(documents[k1].intersection(documents[k2])) / float(len(documents[k2]))
        #self.imshow(Z, '%s-%s-intersections' % (self.topic_tag, self.document_tag), size=20, interpolation='nearest')
        self.pcolor(Z, '%s-%s-intersections' % (self.topic_tag, self.document_tag))
        return Z

    def make_phi_heat_map(self):
        "Make a heat map representing the expected phis."
        K = self.statistics.num_topics_used
        import pylab as P
        P.figure()
        heatmap_categories(self.dpm.exp_phi()[:K], category_names=self.word_ids, distribution_names=map(str, range(K)))
        self.save_fig('expected-phi')
        P.close()

    def make_theta_heat_map(self):
        "Make a heat map representing the expected thetas."
        K = self.statistics.num_topics_used
        import pylab as P
        P.figure()
        if len(self.document_ids) < 30:
            document_ids = self.document_ids
        else:
            document_ids = None
        heatmap_categories(self.dpm.exp_theta()[:,:K], category_names=map(str, range(K)), distribution_names=document_ids)
        self.save_fig('expected-theta')
        P.close()

    def make_heat_maps(self):
        #self.make_topic_KL_heat_map()
        logging.info('Creating topic intersection heat maps')
        self.make_phi_heat_map()
        # self.make_theta_heat_map() normally too many documents to make this sensible
        self.make_topic_word_intersection_heat_map()
        self.make_topic_document_intersection_heat_map()

    def topic_sizes(self):
        'Create a PNG of the topic sizes, i.e. the expected number of occurences from each topic.'
        logging.info('Creating topic size histogram')
        import pylab as P
        P.figure()
        P.bar(xrange(self.statistics.num_topics_used), self.dpm.counts.E_n_k[:self.statistics.num_topics_used])
        P.title('%s sizes' % self.topic_tag)
        P.xlabel('Programs')
        P.ylabel('Sizes')
        self.save_fig('%s-sizes' % self.topic_tag)
        P.close()

    def topic_sizes_log_scale(self):
        'Create a PNG of the topic sizes, i.e. the expected number of occurences from each topic.'
        logging.info('Creating topic size histogram (log scale)')
        import pylab as P
        P.figure()
        P.bar(xrange(self.statistics.num_topics_used), self.dpm.counts.E_n_k[:self.statistics.num_topics_used], log=True)
        P.title('%s sizes (log scale)' % self.topic_tag)
        P.xlabel('Programs')
        P.ylabel('Sizes')
        self.save_fig('%s-sizes-log-scale' % self.topic_tag)
        P.close()

    def _histogram(self, data, count_tag, index_tag):
        import pylab as P
        P.figure()
        num_bins = max(data)-min(data)
        while num_bins > 40:
            num_bins /= 2
        P.hist(data, bins=num_bins)
        P.title('\\# %ss in %ss' % (count_tag, index_tag))
        P.xlabel('\\# %ss' % count_tag)
        P.ylabel('\\# %ss' % index_tag)
        self.save_fig('%s-per-%s' % (count_tag, index_tag))
        P.close()

    def histograms(self):
        'Create PNG histograms of the various statistics.'
        logging.info('Creating word/topic/document histograms')
        self._histogram(
          self.statistics.num_topics_per_document(),
          self.topic_tag,
          self.document_tag
        )
        self._histogram(
          self.statistics.num_documents_per_topic(),
          self.document_tag,
          self.topic_tag
        )
        self._histogram(
          self.statistics.num_words_per_topic(),
          self.word_tag,
          self.topic_tag
        )
        self._histogram(
          self.statistics.num_topics_per_word(),
          self.topic_tag,
          self.word_tag
        )

    def _plot_dist(self, dist, title, tag):
        import pylab as P
        P.figure()
        dist.plot()
        self.save_fig(tag)
        P.close()

    def _dist_plots(self):
        self._plot_dist(self.dpm.q_alpha, 'Alpha', 'alpha')
        self._plot_dist(self.dpm.q_beta, 'Beta', 'beta')
        self._plot_dist(self.dpm.q_gamma, 'Gamma', 'gamma')

    def _log_hyper_info(self, p, name):
        logging.info('%8s: E=%4g; G=%4g; params: %s', name, p.E, p.G, str(p.params()))

    def log_hyper_parameter_info(self):
        'Log some information about the distributions over the hyper-parameters.'
        self._log_hyper_info(self.dpm.q_alpha, 'Alpha')
        self._log_hyper_info(self.dpm.q_beta, 'Beta')
        self._log_hyper_info(self.dpm.q_gamma, 'Gamma')

    def log_topic_info(self, k):
        'Log some general information about topic k.'
        topic_words = self.statistics.words_for_topic(k)
        topic_documents = self.statistics.documents_for_topic(k)
        logging.info('%s: ********************************** %d **********************************', self.topic_tag, k)
        logging.info('Expected # %ss count: %f', self.occurence_tag, self.dpm.counts.E_n_k[k])
        logging.info('Number distinct %ss: %d', self.word_tag, len(topic_words))
        logging.info('%ss: %s', self.word_tag, ', '.join(self.word_ids[w] for w in topic_words))
        logging.info('Number %ss using topic: %d', self.document_tag, len(topic_documents))
        logging.info('%ss: %s', self.document_tag, ', '.join(self.document_ids[d] for d in topic_documents))

    def plot_factor_enrichment(self, k):
        'Plots the enrichment this program has for the various factors.'
        import pylab as P
        fig = P.figure()
        P.figtext(0.03, 0.97, 'Factor enrichment in program %d: %d %ss' % (k, len(self.statistics.words_for_topic(k)), self.word_tag))

        P.subplot(211)
        P.bar(range(self.statistics.dpm.W), self.statistics.dpm.counts.E_n_kw[k])
        P.title('Expected number %ss by %s.' % (self.occurence_tag, self.word_tag))

        P.subplot(212)
        phi = self.dpm.exp_phi()[:self.statistics.num_topics_used]
        Phi = self.dpm.exp_Phi()
        phi_ratio = phi/Phi
        P.bar(range(self.statistics.dpm.W), phi_ratio[k])
        P.title('Enrichment ratio over background %s distribution' % self.word_tag)

        return fig



class DpmInferenceHistory(object):
    "Keeps track of statistics during inference."

    def __init__(self, dpm, summariser):
        
        self.plot = pylab_ioff(self.plot)
        
        self.dpm = dpm
        "The DPM."

        self.summariser = summariser
        "Summary of the DPM."

        self.history = cookbook.DictOfLists()
        "Holds the history of each statistic by name."

        self.stats = {
          'log-likelihood' : {
            'negative log likelihood' : lambda: -self.dpm.log_likelihood(),
          },
          'hyper-parameters' : {
             'E(alpha)' : lambda: self.dpm.q_alpha.E,
             'G(alpha)' : lambda: self.dpm.q_alpha.G,
             'E(beta)'  : lambda: self.dpm.q_beta.E,
             'G(beta)'  : lambda: self.dpm.q_beta.G,
             'E(gamma)' : lambda: self.dpm.q_gamma.E,
             'G(gamma)' : lambda: self.dpm.q_gamma.G,
          },
          'topic-sizes' : {
             'E(words/topic)'     : lambda: numpy.mean(self.summariser.statistics.num_words_per_topic()),
             'E(topics/word)'     : lambda: numpy.mean(self.summariser.statistics.num_topics_per_word()),
             'E(topics/document)' : lambda: numpy.mean(self.summariser.statistics.num_topics_per_document()),
             'E(documents/topic)' : lambda: numpy.mean(self.summariser.statistics.num_documents_per_topic()),
          },
          'num_topics_used' : {
             '\\# topics used' : lambda: self.summariser.statistics.num_topics_used,
          },
        }
        "A dictionary of dictionaries. Top level keys are plot names, second level keys are stats in that plot."

    def iteration(self):
        for plot, stats in self.stats.iteritems():
            for name, fn in stats.iteritems():
                self.history[name].append(fn())
        return -self.history['negative log likelihood'][-1]

    def plot(self):
        import pylab as P
        for plot, stats in self.stats.iteritems():
            P.figure()
            for name, fn in stats.iteritems():
                P.plot(self.history[name], label=name)
            P.legend()
            self.summariser.save_fig(tag='history-%s' % plot)
            P.close()


if '__main__' == __name__:
    plot_categories(categories)


