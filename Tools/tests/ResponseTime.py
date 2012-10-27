from timeit import timeit

number = 10000
print 'Starting tests with %s connections' % number
time = timeit('opener = urllib.FancyURLopener({}); f = opener.open("http://localhost:80/")', 'import urllib;', number=number)
print 'Nginx   : %s' % time

time = timeit('opener = urllib.FancyURLopener({}); f = opener.open("http://localhost:8080/")', 'import urllib;', number=number)
print 'Twisted : %s' % time
print '========================'
print 'FIN'
