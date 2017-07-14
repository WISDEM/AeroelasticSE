def vtree_connect(param_list, self, nm1, nm2):
   for line in open(param_list, 'r').readlines():
      line=line.strip('\n')
      print 'CONNECTING ', ':'.join([nm1, line]), ':'.join([nm2, line])
      self.connect(':'.join([nm1, line]), ':'.join([nm2, line]))
