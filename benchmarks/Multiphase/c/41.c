int main(){
    int x, y;

    // pre-conditions
    x = 0;
    y = 7500;
    

    // loop body
    while(unknown()){
        if(x >= 5000){
            y = y + 1;
        }
        if(x % 2 == 0){
            x = x + 2;
        }else{
            x = x + 1;
        }     
    }

    // post-condition
    if(x == 10000){
        assert(y == 10000);
    }
    
}