int main(){
    int x, y, c0;

    // pre-conditions
    x = 0;
    c0 = 5000;
    y = c0;


    // loop body
    while(unknown()){
        if(x >= c0){
            y = y + 1;
        }else{
            y = y - 1;
        }
        x = x + 1;
    }

    // post-condition
    if(x == (2 * c0)){
        assert(y == c0);
    }
    
}