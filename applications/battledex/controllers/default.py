# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to the Battle-Dex!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def pokefinder():
    
    ptype = ''
    lists= ''
    x= ''
    order =''
    response.flash = "Discover a Pokemon to use for a specific role on your team"
    
        
    if request.vars.stat1:
        stata = request.vars.stat1.lower()
        stataname = request.vars.stat1
        
    if request.vars.stat2:
        statb=request.vars.stat2.lower()
        statbname = request.vars.stat2

    if request.vars.stat1=="SPAttack":
        stataname = "Special Attack"
        
    if request.vars.stat2=="SPAttack":
        statbname = "Special Attack"
        
    if request.vars.stat1=="SPDefense":
        statbname = "Special Defense"
        
    if request.vars.stat2=="SPDefense":
        statbname = "Special Defense"
        
    if request.vars.ptype:
            ptype = request.vars.ptype

            lists = db(db.pkstats.ptype==ptype).select(db.pkstats.ALL, orderby=~(db.pkstats[stata] + db.pkstats[statb]), limitby=(0,30))
            
    if request.vars.ptype=='ANY':
            x = request.vars.ptype
            lists = db(db.pkstats.ptype!=None).select(db.pkstats.ALL, orderby=~(db.pkstats[stata] + db.pkstats[statb]), limitby=(0,30))
            
    
    
    categories = db().select(db.stats.ALL)
    ptypes = db().select(db.types.ALL)         
    
    return locals()

def enemy_analyzer():
    response.flash = "Analyze a Pokemon's crucial points"
    creature = ''
    results = ''
    points= ''
    if request.vars.pokemon:
        term = request.vars.pokemon+'%'
        results = db(db.pkstats.name.like(term)).select(db.pkstats.ALL)

    return locals()

def search_selector():
    results = ''
    if not request.vars.pokemon:
        return ''
    pattern = request.vars.pokemon.capitalize() + '%'
    selected = [row.name for row in db(db.pkstats.name.like(pattern)).select()]
    return ''.join([DIV(k,
                 _onkeyup="jQuery('#pokemon').val('%s')" % k,
                 _onclick="jQuery('#pokemon').val('%s')" % k
                 ).xml() for k in selected])
    return locals()

def me():
    user = db.auth_user(request.args(0) or me)
    return locals()


def battlenow():
    user = db.auth_user(request.args(0) or me)
    return locals()
