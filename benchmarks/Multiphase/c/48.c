int main(){
    int x, y;

    // pre-conditions
    x = 0;
    y = 0;

    // loop body
    while(unknown()){
        if(x < 5000){
            if(x >= 4000){
                y = y + 4;
            }else{
                y = y + 1;
            }
        }else{
            if(x >= 6000){
                y = y - 1;
            }else{
                y = y - 4;
            }
        }
        x = x + 1;
    }

    // post-condition
    if(x == 10000){
        assert(y == 0);
    }
    
}