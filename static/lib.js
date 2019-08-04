state_playerB = 0;  
state_playerA = 0;
number_play   = 0;
global_lvl    = 0;
global_qtable = [];

$('body').on('hidden.bs.modal', '#centralModalSuccess', function(){ 
  $('#review').html('');
  number_play = 0;
if(global_lvl == 2)
    if(Math.random() < 0.5)
      send(99)
});

function set_lvl(lvl){
   global_lvl = lvl
   leg =['Fácil','Médio','Difícil']
   $('#review').html('');
   $('#ia').html('<b>I.A ('+leg[global_lvl]+') </b>')
   
   if(global_lvl == 2)
      send(99)
   else
      update(0,0)  
}  
function set_buttom(row, val){
   if(val == 0){   
       val = ' ';     
       //console.log('set_buttom',row, val, row.substr(0, 3), row.substr(7, 1))
       if( row.substr(0, 3) == 'win')
          val = parseFloat( global_qtable[row.substr(7, 1)-1] ).toFixed(2);
                
       $('#'+row).attr("disabled", false);
   }else{
       $('#'+row).attr("disabled", true);
       if(val == 1)
         val = 'X';
       if(val == 2)
         val = 'O';              
   }   
   $('#'+row).html(val);         
}
function win(player){
   $('#player_win').html('Vencedor : '+player) 
   $('#centralModalSuccess').modal({
     keyboard: false
   }) ;        
}
function send(action){ 
  console.log(action)
  $.post("/handle/"+action+"/"+state_playerB+"/"+state_playerA+"/"+global_lvl, function( data ) {
        play = JSON.parse(data);
        console.log(play);
        state_playerB = play.state_playerB;
        state_playerA = play.state_playerA;
        IA_win        = play.IA_win;
        $('#win'+global_lvl).html(play.IA_win[global_lvl][2]);
        $('#defeat'+global_lvl).html(play.IA_win[global_lvl][1]);
        $('#draw'+global_lvl).html(play.IA_win[global_lvl][0]);

       for(let r in play.rows) 
         set_buttom(r, play.rows[r])  

        number_play++;   
       if(play.done){
            for(let r in play.rows) 
              set_buttom(r, '')   

            if(play.win[1] == 1){
                win('Player')
                update(state_playerA,'win_') 
                feedback(state_playerA, number_play)  
            }else if(play.win[1] == 2){  
                win('I.A')
                update(state_playerB,'win_') 
                feedback(state_playerB, number_play)  
            }else{
                win('Empate')
                update(play.win[0],'win_')   
                feedback(play.win[0], number_play)
            }                
       }else{
          feedback(state_playerA, number_play)
       }  
  });
} 
function feedback(state, number_play){
    $('#review').append('<button id="win_row1" onclick="update('+state+',1)" style="width: 130px;height: 50px;margin: 10px;" type="button" class="btn btn-lg btn-primary" >Jogada #'+number_play+'</button>')
}
function update(state, prefix){     
    prefix = (prefix == 0) ? '' : 'win_';
    $.post("/update/"+state+"/"+global_lvl, function( data ) {
          play = JSON.parse(data);
          //console.log(play);
          state_playerB = play.state_playerB;
          state_playerA = play.state_playerA;
          IA_win        = play.IA_win;
          global_qtable = play.state;
          //console.log(global_qtable)
          $('#win0').html(play.IA_win[0][2]);
          $('#draw0').html(play.IA_win[0][0]);
          $('#defeat0').html(play.IA_win[0][1]);          
          $('#defeat1').html(play.IA_win[1][1]);          
          $('#defeat2').html(play.IA_win[2][1]);          
  
         for(let r in play.rows) 
           set_buttom(prefix+r, play.rows[r])  
    });
} 
update(0,0)