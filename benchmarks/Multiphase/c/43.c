int main(){
    int x, y;

    // pre-conditions
    x = 0;
    y = 0;
    

    // loop body
    while(unknown()){
        if(x >= 50000000){
            if(x >= 100000000){
                y = y;
            }else{
                y = y + 1;
            }
        }else{
            y = 0;
        }
        x = x + 1;
    }

    // post-condition
    if(x >= 100000000){
        assert(y == 50000000);
    }
    
}