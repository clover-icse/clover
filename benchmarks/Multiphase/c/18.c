int main(){
    int x, y;

    // pre-conditions
    x = 1;
    y = 1;

    // loop body
    while(unknown()){
        if(y < 16){
            y = y * 2;
        }else{
            y = x % 16;
        }
        x = x * 2;
        
    }

    // post-condition
    if(x > 16){
        assert(y == 0);
    }
    
}