int main(){
    int x, y;

    // pre-conditions
    x = 0;
    y = 0;

    // loop body
    while(unknown()){
       if(x >= 7500){
            if(x >= 12500){
                y = y -2;
            }else{
                y = y + 1;
            }
       }else{
            if(x >= 2500){
                y = y + 1;
            }else{
                y = y - 2;
            }
       }
        x = x + 1;
    }

    // post-condition
    if(x == 15000){
        assert(y == 0);
    }
    
}