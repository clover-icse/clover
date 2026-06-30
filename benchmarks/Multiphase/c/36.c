int main(){
    int x, y;

    // pre-conditions
    x = -10000;
    y = 0;
    

    // loop body
    while(unknown()){
        if(y > x){
            y = -x;
            x = x + 1;
        }else{
            y = y + 2;
        }
        
    }

    // post-condition
    if(x >= 0){
        assert(x >= (y - 1));
    }
    
}