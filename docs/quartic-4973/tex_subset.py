"""Small fail-closed parser for the pinned appendix, not a general TeX engine."""
import hashlib
import re

FLAGS=dict(GeneralRoots=True,TargetTwo=True,TangentFusion=True,
           SharedSquare=True,FirstNorm=True,ScalarFusion=False)


class TexError(ValueError):
    pass


def need(ok,message):
    if not ok:raise TexError(message)


def clean_comments(text):
    """Replace unescaped comments by spaces, preserving offsets/newlines."""
    out=list(text);i=0
    while i<len(text):
        if text[i]=='%':
            j=i-1
            while j>=0 and text[j]=='\\':j-=1
            if (i-1-j)%2==0:
                while i<len(text) and text[i]!='\n':out[i]=' ';i+=1
                continue
        i+=1
    return ''.join(out)


def select(text,flags=None):
    flags=FLAGS if flags is None else flags
    need(set(flags)==set(FLAGS) and all(type(x) is bool for x in flags.values()),'Exact Boolean feature set required')
    need(flags==FLAGS,'This inventory supports target2+tangent+firstnorm and excludes optional J0')
    text=text.replace('\r\n','\n');clean=clean_comments(text)
    pattern=re.compile(r'\\(if[A-Za-z]+|else|fi)\b')
    out=[];cursor=0;active=True;stack=[]
    for match in pattern.finditer(clean):
        command=match.group(1)
        if command=='iff':continue
        if active:out.append(text[cursor:match.start()])
        else:out.append('\n'*text[cursor:match.start()].count('\n'))
        cursor=match.end()
        if command.startswith('if'):
            name=command[2:];need(name in flags,'Unsupported TeX conditional '+command)
            stack.append((active,flags[name],False));active=active and flags[name]
        elif command=='else':
            need(bool(stack),'Unmatched else');parent,condition,seen=stack[-1]
            need(not seen,'Repeated else');stack[-1]=(parent,condition,True);active=parent and not condition
        else:
            need(bool(stack),'Unmatched fi');active=stack.pop()[0]
    need(not stack,'Unclosed conditional')
    out.append(text[cursor:] if active else '\n'*text[cursor:].count('\n'))
    result=''.join(out)
    need(not re.search(r'\\if(?:GeneralRoots|TargetTwo|TangentFusion|SharedSquare|FirstNorm|ScalarFusion)\b',clean_comments(result)),'Conditional remained')
    return result


def structure(text):
    need(len(text)<=2_000_000,'TeX byte/character bound')
    clean=clean_comments(text);depth=0
    for m in re.finditer(r'\\.|[{}]',clean):
        token=m.group(0)
        if token=='{':depth+=1
        elif token=='}':depth-=1;need(depth>=0,'Unbalanced closing brace')
    need(depth==0,'Unclosed brace')
    token=re.compile(r'\\(begin|end|label)\{([^{}]+)\}')
    stack=[];environments=[];labels={}
    for m in token.finditer(clean):
        command,name=m.groups()
        if command=='begin':stack.append((name,m.start(),m.end()))
        elif command=='end':
            need(bool(stack) and stack[-1][0]==name,'Mismatched environment '+name)
            _,start,header_end=stack.pop()
            environments.append(dict(name=name,start=start,header_end=header_end,end=m.end(),end_start=m.start()))
        else:
            need(name not in labels,'Duplicate label '+name);labels[name]=m.start()
    need(not stack,'Unclosed environment')
    return clean,labels,environments


def theorem_span(text,label):
    clean,labels,envs=structure(text)
    need(label in labels,'Missing label '+label);at=labels[label]
    candidates=[e for e in envs if e['name'] in ('lemma','theorem','proposition','corollary') and e['start']<=at<e['end']]
    need(len(candidates)==1,'Label is not in one theorem statement '+label)
    theorem=candidates[0]
    proofs=sorted((e for e in envs if e['name']=='proof' and e['start']>=theorem['end']),key=lambda e:e['start'])
    need(bool(proofs),'Missing proof '+label);proof=proofs[0]
    need(not clean[theorem['end']:proof['start']].strip(),'Unexpected content before proof '+label)
    return span(text,theorem['start'],proof['end'],label)


def statement_span(text,label):
    _,labels,envs=structure(text)
    need(label in labels,'Missing main label '+label)
    candidates=[e for e in envs if e['name']=='theorem' and e['start']<=labels[label]<e['end']]
    need(len(candidates)==1,'Main label is not in a unique theorem')
    e=candidates[0];return span(text,e['start'],e['end'],label)


def span(text,start,end,label=None):
    payload=text[start:end]
    return dict(label=label,start_character=start,end_character=end,
                first_line=text.count('\n',0,start)+1,last_line=text.count('\n',0,end)+1,
                text_sha256=hashlib.sha256(payload.encode()).hexdigest())


def locate_exact(text,body):
    start=text.find(body)
    need(start>=0 and text.find(body,start+1)<0,'Reviewed selected appendix missing or duplicated')
    return span(text,start,start+len(body))


def project_layout(text):
    """Only whitespace, display breaks and explicit spacing commands may differ."""
    clean=clean_comments(text)
    # Preserve TeX control-word boundaries: stripping whitespace as raw text
    # would incorrectly identify '\\mu x' with the different command '\\mux'.
    tokens=re.findall(r'\\[A-Za-z@]+|\\.|[^\\\s]',clean)
    spacing={r'\qquad',r'\quad',r'\ ',r'\,',r'\;',r'\!',r'\[',r'\]'}
    return tuple(token for token in tokens if token not in spacing)


def layout_edits(text,edits):
    need(isinstance(edits,list) and len(edits)<=20,'Layout edit bound')
    for edit in edits:
        need(set(edit)=={'old','new'},'Layout edit keys')
        old,new=edit['old'],edit['new']
        need(type(old) is str and type(new) is str and 0<len(old)<=4096 and len(new)<=4096,'Layout edit size')
        need(project_layout(old)==project_layout(new),'Layout edit changes mathematical tokens')
        need(text.count(old)==1,'Layout edit target must occur once')
        text=text.replace(old,new)
    return text
