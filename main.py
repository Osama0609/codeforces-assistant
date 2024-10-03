import requests, json, time

class PROBLEM:
    rating = ID = 0
    index = ''
    name = ''
    
    def __lt__(self, other):
        if self.ID == other.ID:
            return self.index < other.index
        return self.ID < other.ID
    def get_str(self):
        res = ''
        res += str(self.ID) + self.index + ', '
        res += self.name + ', '
        res += str(self.rating)
        return res
    
def to_solve_problems(handle):
    
    gyms_link = 'https://codeforces.com/api/contest.list?gym=true'
    requested_gyms = requests.get(gyms_link)
    time.sleep(2)
    
    if requested_gyms.ok == False:
        print('Error')
        exit()
    
    requested_gyms = json.loads(requested_gyms.text)
    
    if requested_gyms['status'] != 'OK':
        print('Error')
        exit()
    
    gyms = {}
    solved = {}
    requested_gyms = requested_gyms['result']
    
    for gym in requested_gyms:
        if gym.get('difficulty') != None:
            gyms[gym['id']] = True
    
    submissions_link = 'https://codeforces.com/api/user.status?handle=' + handle
    requested_submissions = requests.get(submissions_link)
    time.sleep(2)
    
    if requested_submissions.ok == False:
        print('Error')
        exit()
    
    requested_submissions = json.loads(requested_submissions.text)
    
    if requested_submissions['status'] != 'OK':
        print('Error')
        exit()
    
    virtual_gyms = set()
    
    requested_submissions = requested_submissions['result']
    
    for submission in requested_submissions:
        author = submission['author']
        if gyms.get(submission['contestId']) != None and author['participantType'] == 'VIRTUAL':
            virtual_gyms.add(submission['contestId'])
            if submission['verdict'] == 'OK':
                s = str(submission['contestId'])
                p = submission['problem']
                s += p['index']
                solved[s] = True
    
    virtual_gyms = list(virtual_gyms)
    virtual_gyms.sort()
    
    for gym in virtual_gyms:
        standings_link = 'https://codeforces.com/api/contest.standings?contestId='
        standings_link += str(gym)
        standings_link += '&from=1&count=1&showUnofficial=true'
        
        requested_standings = requests.get(standings_link)
        time.sleep(2)
        
        if requested_standings.ok == False:
            print('Error')
            exit()
        
        requested_standings = json.loads(requested_standings.text)
        requested_standings = requested_standings['result']
        
        contest = requested_standings['contest']
        problems = requested_standings['problems']
        
        print(contest['name'], end = ': \n')
        
        for p in problems:
            s = str(p['contestId']) + p['index']
            if solved.get(s) == None:
                print(s, end = ', ')
                print(p['name'])
        print("")
    
def get_solved_during_contest(handle):
    request_link = 'https://codeforces.com/api/user.status?handle=' + handle
    request = requests.get(request_link)
    
    if request.ok == False:
        print('Error')
        exit()
    
    request = json.loads(request.text)
    
    if request['status'] != 'OK':
        print('Error')
        exit()
    
    result = request['result']
    
    in_competition = set()
    out_of_competition = set()
    
    def compare(a):
        return a.rating
    
    for submission in result:
        problem = submission['problem']
        author = submission['author']
        
        if problem.get('problemsetName') == 'acmsguru' or submission['verdict'] != 'OK' or problem.get('rating') == None:
            continue
        
        if author['participantType'] != 'CONTESTANT' and author['participantType'] != 'OUT_OF_COMPETITION':
            continue
        
        p = PROBLEM()
        
        p.rating = problem.get('rating')
        p.ID = problem.get('contestId')
        p.index = problem.get('index')
        p.name = problem.get('name')

        if author['participantType'] == 'CONTESTANT':
            in_competition.add(p)
        else:
            out_of_competition.add(p)
    
    in_competition = list(in_competition)
    out_of_competition = list(out_of_competition)
    
    in_competition.sort(key = compare)
    out_of_competition.sort(key = compare)
    
    print('Out of competition ACs:')
    print('Count = ', end = ' ')
    print(len(out_of_competition))
    
    for pr in out_of_competition:
        print(pr.get_str())
    
    print('\n')    
    
    print('Official ACs:')
    print('Count = ', end = ' ')
    print(len(in_competition))
    
    for pr in in_competition:
        print(pr.get_str())
    
def get_solved_problems(handle):
    
    print('Enter the tag (or the word "all" if there is no specific tag):')
    tag = str(input())
    
    print('Enter the minimum rating: ')
    min_rate = int(input())
    print('Enter the maximum rating:')
    max_rate = int(input())
    
    problems_link = 'https://codeforces.com/api/problemset.problems?tags='
    submissions_link = 'https://codeforces.com/api/user.status?handle='
    
    if tag == 'all':
        problems_link = 'https://codeforces.com/api/problemset.problems'
        tag = ''
    
    requested_problems = requests.get(problems_link + tag)
    
    if requested_problems.ok == False:
        print('Error')
        exit()
        
    time.sleep(1)
        
    requested_submissions = requests.get(submissions_link + handle)
    
    if requested_submissions.ok == False:
        print('Error')
        exit()
    
    result = json.loads(requested_problems.text)
    
    if result['status'] != 'OK':
        print('Error')
        exit()
        
    problems_list = result['result']
    
    result = json.loads(requested_submissions.text)
    
    if result['status'] != 'OK':
        print('Error')
        exit()
        
    submissions_list = result['result']
    problems_list = problems_list['problems']
    
    solved = {}
    
    for submission in submissions_list:
        if submission['verdict'] == 'OK':
            problem = submission['problem']
            
            if problem.get('problemsetName') == 'acmsguru':
                continue
            
            ID = str(problem['contestId']) + problem['index']
            solved[ID] = True
    
    result = []
    
    for problem in problems_list:
        now = PROBLEM()
        ID = str(problem['contestId']) + problem['index']
        
        if problem.get('problemsetName') == 'acmsguru' or problem.get('rating') == None:
            continue
        
        if problem['rating'] < min_rate or problem['rating'] > max_rate:
            continue
        
        if solved.get(ID) == True:
            now.rating = problem['rating']
            now.ID = problem['contestId']
            now.index = problem['index']
            now.name = problem['name']
            result.append(now)
    
    result.sort()
    print('The number of solved problems in the given rage is:', end = ' ')
    print(len(result))
    
    for res in result:
        print(res.get_str())

def ignore_negative_rating_changes(handle):
    
    contests_link = 'https://codeforces.com/api/user.rating?handle='

    requested_contests = requests.get(contests_link + handle)

    if requested_contests.ok == False:
        print('Connection Error')
        exit()
        
    json_contests = json.loads(requested_contests.text)

    if json_contests['status'] != 'OK':
        print("No such handle")
        exit()
    
    old_rating = 0
    contests_list = json_contests['result']
    
    for i in range(0, len(contests_list)):


        contest = contests_list[i]
        contest['rating_change'] = contest['newRating'] - old_rating
        
        contest['performance'] = old_rating + 4 * contest['rating_change']
        old_rating += contest['rating_change']
        contests_list[i] = contest
    
    old_rating = 0
    
    for i in range(0, len(contests_list)):
        contest = contests_list[i]
        rc = int(int(contest['performance'] - old_rating) / 4)
        
        if rc >= 0:
            print(contest['contestName'], end = ': ')
            print(old_rating, end = ' ==> ')
            
            old_rating += rc
            
            print(old_rating, end = ' | ')
            print('Rank = ' + str(contest['rank']) + ', Rating Change = +' + str(rc))

print('Enter your CF handle:', end = ' ')
handle = str(input())

print('Type:')
print('\t"1" to get a list of all problems solved during a cntest.')
print('\t"2" to get a list of all problems that were not solved during a virtual participation (GYMs only).')
print('\t"3" to get a list of all solved problems in a difficulty range.')
print('\t"4" to see what your rating will be if we ignore any contest that makes your rate decrease.')

todo = str(input())

if todo == '1':
    get_solved_during_contest(handle)

elif todo == '2':
    to_solve_problems(handle)

elif todo == '3':
    get_solved_problems(handle)
    
elif todo == '4':
    ignore_negative_rating_changes(handle)
    
else:
    print('Invalid Input')
