int main(){
    int x, y;

    // pre-conditions
    x = 0;
    

    // loop body
    while(unknown()){
        if(x == 1000){
            y = 0;
        }

        if(x / 5 < 200){
            x = x + 1;
        }else{
            x = x + 5;
        }
    }

    // post-condition
    if(x >= 2000){
        assert(y == 0);
    }
    
}