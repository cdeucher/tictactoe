state_playerB = 0;  
state_playerA = 0
number_play   = 0

function set_buttom(row, val){
   if(val == 0){
       val = ' ';
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
   $('body').on('hidden.bs.modal', '#centralModalSuccess', function(){ 
        $('#review').html('');
        number_play = 0;
   });       
}
function send(action){ 
  $.post("/handle/"+action+"/"+state_playerB+"/"+state_playerA, function( data ) {
        play = JSON.parse(data);
        console.log(play);
        state_playerB = play.state_playerB;
        state_playerA = play.state_playerA;
        IA_win        = play.IA_win;
        $('#win').html(play.IA_win[2]);
        $('#defeat').html(play.IA_win[1]);
        $('#draw').html(play.IA_win[0]);

       for(let r in play.rows) 
         set_buttom(r, play.rows[r])  

        number_play++;   
       if(play.done){
            for(let r in play.rows) 
              set_buttom(r, '')           
            if(play.win == 1){
                win('Player')
                update(state_playerA,'win_') 
                feedback(state_playerA, number_play)  
            }else if(play.win == 2){  
                win('I.A')
                update(state_playerB,'win_') 
                feedback(state_playerB, number_play)  
            }else{
                win('Empate')
                update(state_playerA,'win_')   
                feedback(state_playerA, number_play)
            }                
       }else{
          feedback(state_playerB, number_play)
       }  
  });
} 
function feedback(state, number_play){
    $('#review').append('<button id="win_row1" onclick="update('+state+',1)" style="width: 130px;height: 50px;margin: 10px;" type="button" class="btn btn-lg btn-primary" >Jogada #'+number_play+'</button>')
}
function update(state, prefix){ 
    prefix = (prefix == 0) ? '' : 'win_';
    $.post("/update/"+state, function( data ) {
          play = JSON.parse(data);
          console.log(play);
          state_playerB = play.state_playerB;
          state_playerA = play.state_playerA;
          IA_win        = play.IA_win;
          $('#win').html(play.IA_win[2]);
          $('#defeat').html(play.IA_win[1]);
          $('#draw').html(play.IA_win[0]);
  
         for(let r in play.rows) 
           set_buttom(prefix+r, play.rows[r])  
    });
} 
update(0,0)