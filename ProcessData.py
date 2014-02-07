import sys

from hmmEM import em

filename = '../Data/ManchesterDataset.txt'
problemsets = ['Manchester Fractions Study 2013 Comparison']


file = open(filename)
file.readline()
row = file.readline().split('\t')
curr_student = row[2]
curr_prob = None
# i = 0 # Student id
# a = 0 # Action id
actions = [[]]
obs = [[]]
fakeSteps = ['', '_root goToStep', 'done ButtonPressed', None]
while row != ['']:
	if row[3] != curr_student and row[13] in problemsets:
		curr_student = row[3]
		curr_prob = None
		if len(obs) > 0 and [] in obs[-1]:
			actions[-1].pop(-1)
			obs[-1].pop(-1)
		actions.append([])
		obs.append([])
		# i += 1
		continue
	if row[13] not in problemsets:
		row = file.readline().split('\t')
		continue
	if row[14] != curr_prob:
		curr_prob = row[14]
		# a += 1
		if not (len(obs[-1]) > 0 and obs[-1][-1] == []):
			obs[-1].append([])
		else:
			actions[-1].pop(-1)
		actions[-1].append(int(curr_prob))
		fakeSteps = fakeSteps[0:3]
	if row[17] not in fakeSteps:
		obs[-1][-1].append(1 if row[19] == 'Correct' else 0)
		# fakeSteps[-1] = row[16] # In case the previous step was InCorrect, we don't want to double count it.
	# elif row[16] != fakeSteps[-1]:
	# 	fakeSteps[-1] = None
		fakeSteps.append(row[17])
	row = file.readline().split('\t')

file.close()

# Can be used when observations are "ternary" -- 0 for incorrect, 1 for correct, 2 for hint

# def ter2bin(terlst):
# 	binlst = []
# 	carry = 0
# 	for num in terlst:
# 		binlst.append((num + carry) % 2)
# 		carry = (num + carry)/2
# 	binlst.append(carry)
# 	return binlst

# binobs = []
# for e in obs:
# 	binobs.append([])
# 	for lst in e:
# 		binobs[-1].append(ter2bin(lst))

# Can be used to convert observation from 0-1 vector to a decimal number

def bin2dec(terlst):
	tot = 0
	for (i, num) in enumerate(terlst):
		tot += num * 2**(len(terlst) - i - 1)
	return tot

# decobs = []
# for s in obs:
# 	decobs.append([])
# 	for lst in s:
# 		decobs[-1].append(bin2dec(lst))

opa = [0 for i in range(36)]
for i in range(len(actions)):
	for j in range(len(actions[i])):
		actions[i][j] = actions[i][j] - 1
		# opa[actions[i][j]] = min(2**(len(obs[i][j]) + 1) - 1,31)
		opa[actions[i][j]] = 2

# newobs will be 0 if less than half the steps were correct and 1 otherwise.		
newobs = []
for o in obs:
	newobs.append(map(lambda e: int(e.count(1) > len(e)/2.), o))
print newobs

print em(newobs[1:], actions[1:], 4, 36, opa, 5)