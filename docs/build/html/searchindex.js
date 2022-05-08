Search.setIndex({docnames:["accounts","blackjack","craps","games","index","menus","playing_cards","utils"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":4,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":3,"sphinx.domains.rst":2,"sphinx.domains.std":2,sphinx:56},filenames:["accounts.rst","blackjack.rst","craps.rst","games.rst","index.rst","menus.rst","playing_cards.rst","utils.rst"],objects:{"accounts.admin":{CustomUserAdmin:[0,1,1,""]},"accounts.admin.CustomUserAdmin":{add_form:[0,2,1,""],fieldsets:[0,2,1,""],model:[0,2,1,""]},"accounts.forms":{AddFundsBankForm:[0,1,1,""],AddFundsCryptoForm:[0,1,1,""],CustomAuthenticationForm:[0,1,1,""],CustomPasswordResetForm:[0,1,1,""],CustomUserCreationForm:[0,1,1,""],RequestForm:[0,1,1,""],WithdrawForm:[0,1,1,""]},"accounts.forms.AddFundsBankForm":{clean:[0,3,1,""],media:[0,4,1,""]},"accounts.forms.AddFundsCryptoForm":{clean:[0,3,1,""],media:[0,4,1,""]},"accounts.forms.CustomAuthenticationForm":{media:[0,4,1,""]},"accounts.forms.CustomPasswordResetForm":{media:[0,4,1,""]},"accounts.forms.CustomUserCreationForm":{Meta:[0,1,1,""],media:[0,4,1,""],save:[0,3,1,""]},"accounts.forms.CustomUserCreationForm.Meta":{model:[0,2,1,""]},"accounts.forms.RequestForm":{media:[0,4,1,""]},"accounts.forms.WithdrawForm":{clean:[0,3,1,""],media:[0,4,1,""]},"accounts.models":{CustomUser:[0,1,1,""]},"accounts.models.CustomUser":{DoesNotExist:[0,5,1,""],MultipleObjectsReturned:[0,5,1,""],deposit:[0,3,1,""],update_balance:[0,3,1,""],withdraw:[0,3,1,""]},"accounts.views":{AccountView:[0,1,1,""],AddFundsBankView:[0,1,1,""],AddFundsCryptoView:[0,1,1,""],CustomLoginView:[0,1,1,""],FriendsView:[0,1,1,""],SignUpView:[0,1,1,""],withdraw_funds:[0,6,1,""]},"accounts.views.AddFundsBankView":{form_class:[0,2,1,""],form_valid:[0,3,1,""],get_form_kwargs:[0,3,1,""]},"accounts.views.AddFundsCryptoView":{form_class:[0,2,1,""],form_valid:[0,3,1,""],get_form_kwargs:[0,3,1,""]},"accounts.views.CustomLoginView":{form_class:[0,2,1,""],post:[0,3,1,""]},"accounts.views.SignUpView":{form_class:[0,2,1,""],form_valid:[0,3,1,""]},"games.blackjack.game":{blackjack:[1,0,0,"-"],utils:[1,0,0,"-"]},"games.blackjack.game.blackjack":{Blackjack:[1,1,1,""],BlackjackRound:[1,1,1,""]},"games.blackjack.game.blackjack.Blackjack":{add_player:[1,3,1,""],add_players_from_waiting_room:[1,3,1,""],all_ready:[1,3,1,""],check_update_game_stage:[1,3,1,""],dict_representation:[1,3,1,""],get_stage:[1,3,1,""],ready_up:[1,3,1,""],record_bet:[1,3,1,""],record_bets:[1,3,1,""],remove_player:[1,3,1,""],reset:[1,3,1,""],start_round:[1,3,1,""]},"games.blackjack.game.blackjack.BlackjackRound":{check_dealers_turn:[1,3,1,""],check_for_blackjack:[1,3,1,""],dict_representation:[1,3,1,""],get_stage:[1,3,1,""],initialize_hand:[1,3,1,""],make_player_ready:[1,3,1,""],payout_hand:[1,3,1,""],play_dealer:[1,3,1,""],remove_player:[1,3,1,""],update_game:[1,3,1,""]},"games.blackjack.game.utils":{BlackjackCard:[1,1,1,""],BlackjackHand:[1,1,1,""],Dealer:[1,1,1,""],Pack:[1,1,1,""]},"games.blackjack.game.utils.BlackjackCard":{get_value:[1,3,1,""]},"games.blackjack.game.utils.BlackjackHand":{calculate_outcome:[1,3,1,""],hit:[1,3,1,""],to_list:[1,3,1,""],value:[1,3,1,""]},"games.blackjack.game.utils.Dealer":{play_hand:[1,3,1,""]},"games.blackjack.game.utils.Pack":{build:[1,3,1,""],check_reshuffle:[1,3,1,""],deal:[1,3,1,""],shuffle:[1,3,1,""]},"games.blackjack.web":{consumers:[1,0,0,"-"]},"games.blackjack.web.consumers":{BlackjackConsumer:[1,1,1,""],BlackjackUpdater:[1,1,1,""]},"games.blackjack.web.consumers.BlackjackConsumer":{connect:[1,3,1,""],disconnect:[1,3,1,""]},"games.blackjack.web.consumers.BlackjackUpdater":{load_game:[1,3,1,""],make_move:[1,3,1,""],place_bet:[1,3,1,""],ready_up:[1,3,1,""],request_user_balance:[1,3,1,""]},"games.craps.game":{craps:[2,0,0,"-"]},"games.craps.game.craps":{CrapsGame:[2,1,1,""]},"games.craps.game.craps.CrapsGame":{add_player:[2,3,1,""],add_players_from_waiting_room:[2,3,1,""],all_ready:[2,3,1,""],calculate_payouts:[2,3,1,""],choose_next_shooter:[2,3,1,""],dict_representation:[2,3,1,""],get_stage:[2,3,1,""],ready_up:[2,3,1,""],remove_player:[2,3,1,""],reset:[2,3,1,""],start_round:[2,3,1,""],unready_all:[2,3,1,""],update_come_bets:[2,3,1,""],update_pass_bets:[2,3,1,""]},"games.craps.web":{consumers:[2,0,0,"-"]},"games.craps.web.consumers":{CrapsConsumer:[2,1,1,""],CrapsUpdater:[2,1,1,""]},"games.craps.web.consumers.CrapsConsumer":{connect:[2,3,1,""],disconnect:[2,3,1,""],receive:[2,3,1,""]},"games.craps.web.consumers.CrapsUpdater":{FUNCTION_MAP:[2,2,1,""],come_out_roll:[2,3,1,""],load_game:[2,3,1,""],place_bet1:[2,3,1,""],place_bet2:[2,3,1,""],point_roll:[2,3,1,""],ready1:[2,3,1,""],ready2:[2,3,1,""],ready_restart:[2,3,1,""],user_balance:[2,3,1,""]},"menus.views":{BlackjackRules:[5,1,1,""],BlackjackSessions:[5,1,1,""],CrapsRules:[5,1,1,""],CrapsSessions:[5,1,1,""],Index:[5,1,1,""],PokerRules:[5,1,1,""],PokerSessions:[5,1,1,""],RouletteRules:[5,1,1,""],RouletteSessions:[5,1,1,""],SlotsRules:[5,1,1,""],SlotsSessions:[5,1,1,""]},"menus.views.BlackjackSessions":{post:[5,3,1,""]},"menus.views.CrapsSessions":{post:[5,3,1,""]},"menus.views.PokerSessions":{post:[5,3,1,""]},"menus.views.RouletteSessions":{post:[5,3,1,""]},"menus.views.SlotsSessions":{post:[5,3,1,""]},"utils.PlayingCards.card":{Card:[6,1,1,""]},"utils.PlayingCards.deck":{Deck:[6,1,1,""]},"utils.PlayingCards.rank":{Rank:[6,1,1,""]},"utils.PlayingCards.suit":{Suit:[6,1,1,""]},accounts:{admin:[0,0,0,"-"],forms:[0,0,0,"-"],models:[0,0,0,"-"],views:[0,0,0,"-"]},menus:{views:[5,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","property","Python property"],"5":["py","exception","Python exception"],"6":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:property","5":"py:exception","6":"py:function"},terms:{"0":1,"1":2,"10":0,"17":1,"2":1,"21":1,"25":0,"36":0,"75":1,"9":0,"boolean":[0,2],"byte":2,"case":[0,2],"class":[0,1,2,5,6],"do":0,"float":[0,1,2],"function":[0,1,2],"int":[1,2],"new":[0,1],"public":0,"return":[0,1,2],"static":[1,2],"true":[0,1,2],A:[0,1,2],As:2,For:[0,2],If:[0,2],In:2,The:[0,1,2],Then:0,There:2,Will:0,__all__:0,abl:2,account:[1,2,4],accountview:0,action:1,actual:2,ad:[0,1,2],add:[0,1,2],add_form:0,add_play:[1,2],add_players_from_waiting_room:[1,2],addfundsbankform:0,addfundsbankview:0,addfundscryptoform:0,addfundscryptoview:0,addit:2,address:0,adjust:0,admin:4,admin_sit:0,advanc:0,after:[0,2],again:2,alia:0,all:[0,1,2],all_readi:[1,2],allow:2,also:0,amount:[0,1,2],an:[0,2],ani:[0,1,2],append:1,appropri:[0,2],ar:[0,1,2],area:2,arg:[0,1,2,5],associ:[0,2],awai:[1,2],back:[0,2],balanc:[0,1,2],bank:0,base:1,been:[0,2],being:2,bet:[1,2],between:0,bio:0,birthdai:0,blackjack:[3,4,5],blackjackcard:1,blackjackconsum:1,blackjackhand:1,blackjackround:1,blackjackrul:5,blackjacksess:5,blackjackupdat:1,board:2,bool:[0,1,2],build:1,button:2,bytes_data:2,calcul:[1,2],calculate_outcom:1,calculate_payout:2,call:[0,2],can:2,card:[1,4,7],card_class:[1,6],casino:0,certain:[0,2],chang:[0,1,2],channel:[1,2],charact:0,check:[0,1,2],check_dealers_turn:1,check_for_blackjack:1,check_reshuffl:1,check_update_game_stag:1,choos:2,choose_next_shoot:2,chosen:[1,2],clean:0,cleaned_data:0,code:[1,2],come:2,come_bet:2,come_out_rol:2,commit:0,compar:1,complet:0,complic:2,condit:2,configur:0,connect:[1,2],consum:3,consumerupdat:2,contain:[0,1,2],continu:2,cord:1,core:0,crap:[3,4,5],crapsconsum:2,crapsgam:2,crapsround:2,crapsrul:5,crapssess:5,crapsupdat:2,creat:[0,2],crypto:0,current:[0,1,2],customauthenticationform:0,customloginview:0,custompasswordresetform:0,customus:[0,1,2],customuseradmin:0,customusercreationform:0,data:[0,2],databas:0,date:0,deal:1,dealer:1,dealt:1,decid:2,decis:1,deck:[1,7],decrement:0,defin:[0,2],deposit:0,deposit_amount:0,desir:2,detail:2,determin:2,dice:2,dict:[0,1,2],dict_represent:[1,2],dictionari:[0,1,2],differ:2,digit:0,direct:2,disconnect:[1,2],displai:[0,2,5],distribut:2,django:0,docstr:2,doe:1,doesnotexist:0,dollar:0,don:2,done:2,dont_come_bet:2,dont_pass_bet:2,doubl:2,dure:2,e:2,each:[0,2],earn:0,edit:0,element:2,email:0,end:[1,2],enter:2,essenti:2,evalu:1,everi:[0,2],everyon:2,exact:2,exce:0,except:[0,2],exist:0,exit:[1,2],extens:2,extra:[0,2],fals:[0,1,2],feasibl:2,field:0,fieldset:0,file:2,fill:1,finish:2,first:[0,2],form:4,form_class:0,form_valid:0,friendsview:0,from:[0,1,2],front:1,full:1,function_map:2,fund:0,game:[0,1,2,4,5],game_inst:1,gameconsum:2,gameplai:2,get:2,get_form_kwarg:0,get_stag:[1,2],get_valu:1,given:2,gotten:2,green:2,ha:[0,1,2],hand:1,handl:[0,1,2,5],handler:0,have:[0,2],here:2,hit:[1,2],hook:0,how:1,howev:2,html:[0,2,5],http:0,httprespons:0,i:2,id:2,identifi:0,includ:[0,2],increment:0,index:[0,4,5],indic:0,individu:2,inform:0,inherit:0,initi:[1,2],initialize_hand:1,input:[0,2],instanc:[0,2],instanti:0,instruct:2,integ:1,interfac:[0,2],javascript:2,js:2,just:2,kei:2,kwarg:[0,1,2,5],last:[0,2],left:2,level:0,like:[1,2],limit:0,line:2,link:0,list:[1,2],listen:2,load:[1,2],load_gam:[1,2],log:0,logic:2,made:2,make:1,make_mov:1,make_player_readi:1,map:2,media:0,menu:4,messag:2,met:0,meta:0,method:0,might:2,model:[1,2,4],modul:4,monei:0,month:0,monthli:0,more:2,move:1,much:1,multipl:1,multipleobjectsreturn:0,must:2,name:0,navig:[1,2],necessari:2,necessit:2,need:[1,2],neg:0,new_card:1,next:[0,1,2],non:2,none:[0,1,2],normal:2,num_deck:1,number:0,object:[0,2],odd:2,offici:2,one:[0,2],onli:2,onlin:0,option:[0,2],order:2,other:2,otherwis:[0,1,2],our:0,out:[1,2],outcom:1,over:[0,1,2],overrid:2,overwrit:0,pack:1,page:[0,1,2,4,5],pai:[1,2],param:[0,1],paramet:[0,1,2],parent:2,part:1,particular:0,pass:[0,2],pass_bet:2,password:0,payment:2,payout:2,payout_hand:1,phase:2,place:1,place_bet1:2,place_bet2:2,place_bet:1,plai:[1,4,7],play_deal:1,play_hand:1,player:[1,2],players_readi:2,playingcard:[1,6],point:2,point_rol:2,poker:5,pokerrul:5,pokersess:5,posit:0,post:[0,5],present:2,privat:0,process:[0,2],progress:2,proper:2,properti:0,py:0,rais:0,random:2,randomli:2,rank:[1,7],re:[1,2],readi:[1,2],ready1:2,ready2:2,ready_restart:2,ready_st:[1,2],ready_up:[1,2],realli:2,receiv:2,record:1,record_bet:1,redirect:0,refresh:0,regist:[1,2],remov:[0,1,2],remove_play:[1,2],render:0,replac:2,repres:[0,2],represent:[1,2],request:[0,1,2,5],request_data:[1,2],request_user_bal:[1,2],requestform:0,requir:0,reset:[0,1,2],reshuffl:1,respons:[0,2],rest:2,restart:2,result:2,reveal:2,role:2,roll:2,room:[1,2],roulett:5,rouletterul:5,roulettesess:5,round:[1,2],rout:[0,2],rule:5,run:2,s:[0,1,2],same:2,save:0,screen:2,search:4,second:2,see:1,self:0,send:2,sent:2,session:[1,2],session_id:[1,2],set:2,shooter:2,shown:2,shuffl:1,shuffle_pct:1,signup:0,signupview:0,simpl:2,simpli:[0,2,5],sinc:2,skill:0,slot:5,slotsrul:5,slotssess:5,so:2,socket:[1,2],some:2,special:[0,2],specifi:0,stage:[1,2],stai:1,start:[1,2],start_round:[1,2],state:[1,2],statu:1,still:2,store:2,str:[1,2],string:[1,2],submiss:0,subtract:2,succeed:0,success:0,suit:[1,7],suppli:0,system:2,t:2,take:2,taken:2,text_data:2,thei:[1,2],them:[0,1,2],thi:[0,1,2],those:2,till:1,time:0,to_al:2,to_list:1,top:2,total:0,transact:0,transit:2,turn:1,twice:2,two:1,type:[0,2],typic:0,union:1,unless:2,unord:2,unreadi:2,unready_al:2,until:2,up:[1,2],updat:[0,1,2],update_amount:0,update_bal:0,update_come_bet:2,update_gam:1,update_pass_bet:2,upon:0,url:0,us:[0,1,2],user:[0,1,2],user_bal:2,usercreationform:0,usernam:[0,2],util:[3,4,6],uuid:[1,2],valid:0,validationerror:0,valu:[0,1,2],variabl:0,via:0,view:4,wa:[0,1],wait:[1,2],wallet:0,we:2,web:[0,1,2],websocket:1,well:[0,2],were:1,what:2,when:[1,2],where:2,whether:[0,1,2],which:[0,2],who:1,whose:2,wide:0,widget:0,withdraw:0,withdraw_amount:0,withdraw_fund:0,withdrawform:0,word:2,wsgi:0,wsgirequest:0,yet:2,you:2},titles:["Accounts","Blackjack","Craps","Games","Welcome to OnlineCasino\u2019s documentation!","Menus","Playing Cards","Utils"],titleterms:{account:0,admin:0,blackjack:1,card:6,consum:[1,2],content:[3,4,7],crap:2,deck:6,document:4,form:0,game:3,indic:4,menu:5,model:0,onlinecasino:4,plai:6,rank:6,s:4,suit:6,tabl:4,util:[1,7],view:[0,5],welcom:4}})