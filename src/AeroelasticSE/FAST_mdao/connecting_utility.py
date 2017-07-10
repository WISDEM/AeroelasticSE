def vtree_connect(self, nm1, nm2):
   for line in open('param_list.txt', 'r').readlines():
      line=line.strip('\n')
      self.connect(':'.join([nm1, line]), ':'.join([nm2, line]))
